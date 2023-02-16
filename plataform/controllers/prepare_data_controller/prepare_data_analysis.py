
# from plataform.controllers.process_data_controller.process_data_candles import Process_data_candles
from plataform.controllers.process_data_controller.process_data_candles_versioned import Process_data_candles
from plataform.models.insert_analysis import insert_analysis
from plataform.models.update_operations import update_operations

class PrepareDataAnalysis:
    def analysis_data(request_id, message):
        object_analyzed = Process_data_candles(request_id=request_id).process_data_candles(message=message)
        if object_analyzed["process_action"] == "analysis" and object_analyzed["direction"] != "-":
            insert_analysis(object_analysis=object_analyzed)
            
        elif object_analyzed["process_action"] == "checking_results_operations":
            update_operations(obtect_check_operation=object_analyzed)
            


