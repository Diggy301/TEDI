from  pandas import DataFrame
import chipwhisperer.analyzer as cwa
from PyQt5.QtCore import pyqtSignal, QObject
import pandas as pd

class Analysis(QObject):
    updated_results_table = pyqtSignal(DataFrame)
    update_status_table = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, proj, model, sad_min, sad_max, sad_shift, dtw_rad, key):
        super(Analysis,self).__init__()
        self.proj = proj
        self.analysis_model = model
        self.sad_window_min = sad_min
        self.sad_window_max = sad_max
        self.sad_max_shift = sad_shift
        self.dtw_radius = dtw_rad
        self.key = key

        self.current_analysis = None
        self.current_trace_iteration = 0
        self.apply_sad_resync_flag = False
        self.apply_dtw_resync_flag = False

        self.key_from_round10 = False
        


    def run_analysis(self):
        if self.proj is None:
            print("project undefined") # TODO - should be popup alertt
            return 
            
        if self.analysis_model is None:
            print("Analysis model not defined")
            return

        if self.apply_sad_resync_flag:            
            self.apply_sad_resync()
        if self.apply_dtw_resync_flag:
            self.apply_dtw_resync()


        self.current_analysis = cwa.cpa(self.proj, self.analysis_model)

        results = self.current_analysis.run(self.analysis_callback)
        self.finished.emit()
        
        #save results in text file
        maxs = results.find_maximums()
        df = DataFrame(maxs).transpose()
        df.to_string('results.txt',index = False)
        

    def analysis_callback(self):
        results = self.current_analysis.results
        stat_data = results.find_maximums()
        df = DataFrame(stat_data).transpose()

        
        reporting_interval = self.current_analysis.reporting_interval
        tstart = self.current_trace_iteration * reporting_interval
        tend = tstart + reporting_interval
        self.current_trace_iteration += 1
        caption = f"Finished traces {tstart} to {tend}"

        self.update_status_table.emit(caption)

        #self.updated_results_table.emit(df.head())

        if not self.key_from_round10:
            self.updated_results_table.emit(df.head())
            return

        # IN CASE OF CTR: the key retrieved from results is the output of the 10th round of encryption
        # The following code creates a new dataframe with same correlation values, but keybyte values are exchanged by 
        # the initial key, instead of the 10th round key
        dfh = df.head()
        newdf = pd.DataFrame()
        for row in dfh.values.tolist():
            keyguess = list(list(zip(*row))[0])
            originalkeyguess = cwa.attacks.models.aes.key_schedule.key_schedule_rounds(keyguess, 10, 0)
            newrow = []
            for i, cell in enumerate(row):
                newrow.append((originalkeyguess[i], cell[1], cell[2]))
            newdf = newdf.append(pd.DataFrame([newrow], columns=df.columns), ignore_index=True)

        self.updated_results_table.emit(newdf)


    def apply_sad_resync(self):
        resync_traces = cwa.preprocessing.ResyncSAD(self.proj)
        resync_traces.ref_trace = 0
        resync_traces.target_window = (self.sad_window_min, self.sad_window_max)
        resync_traces.max_shift = self.sad_max_shift
        self.proj = resync_traces.preprocess()

    def apply_dtw_resync(self):
        resync_traces = cwa.preprocessing.ResyncDTW(self.proj)
        resync_traces.ref_trace = 0
        resync_traces.radius = self.dtw_radius
        self.proj = resync_traces.preprocess()

    