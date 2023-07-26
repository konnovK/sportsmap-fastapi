# from logging import Handler, LogRecord
# import time
#
# import yandexcloud
# from yandex.cloud.logging.v1.log_ingestion_service_pb2_grpc import LogIngestionServiceStub, LogIngestionService
# from yandex.cloud.logging.v1.log_ingestion_service_pb2 import WriteRequest
# from google.protobuf.timestamp_pb2 import Timestamp
#
#
# def _yandex_write_log(sdk: yandexcloud.SDK, log_group_id: str, log_seconds: int, log_level: str, log_message: str):
#     entry = {
#         'timestamp': Timestamp(seconds=log_seconds),
#         'level': log_level,
#         'message': log_message
#     }
#
#     log_group_service: LogIngestionService = sdk.client(LogIngestionServiceStub)
#     log_group_service.Write(WriteRequest(destination={'log_group_id': log_group_id}, entries=[entry]))
#
#
# class YandexHandler(Handler):
#     """
#     Хендлер для логгера, который отправляет сообщения в Yandex Cloud Logging.
#     Использует Yandex Cloud SDK for Python.
#
#     https://cloud.yandex.ru/docs/logging/
#     https://cloud.yandex.ru/docs/functions/lang/python/sdk
#     """
#     def __init__(self, sdk: yandexcloud.SDK, log_group_id: str, level=0) -> None:
#         self.sdk = sdk
#         self.log_group_id = log_group_id
#         super().__init__(level)
#
#     def emit(self, record: LogRecord) -> None:
#         log_seconds = int(time.time())
#         log_level = record.levelname
#         match record.levelname:
#             case "WARNING":
#                 log_level = "WARN"
#             case _:
#                 pass
#         log_message = record.msg
#         _yandex_write_log(self.sdk, self.log_group_id, log_seconds, log_level, log_message)
