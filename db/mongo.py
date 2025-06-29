from motor.motor_asyncio import AsyncIOMotorClient
from mcp_Server.core.config import config_env_manager as config
from beanie import init_beanie
from mcp_Server.models.mongo_history import History
print("MongoDB initialized with database: ", config.MONGO_URI)


# def get_mongo_client():
#     return AsyncIOMotorClient(
#         config.MONGO_URI,  # URI kết nối MongoDB, ví dụ: "mongodb://user:pass@host:port/db"

#         maxPoolSize=config.MONGO_MAX_POOL_SIZE,  # Số kết nối tối đa client giữ trong pool (mặc định 100)

#         minPoolSize=config.MONGO_MIN_POOL_SIZE,  # Số kết nối tối thiểu giữ luôn (tốt cho hiệu suất cao)

#         connectTimeoutMS=config.MONGO_CONNECT_TIMEOUT_MS,  # Timeout (ms) khi thiết lập kết nối tới MongoDB

#         serverSelectionTimeoutMS=config.MONGO_SERVER_SELECTION_TIMEOUT_MS,  # Timeout (ms) để chọn 1 server (primary/replica)

#         socketTimeoutMS=config.MONGO_SOCKET_TIMEOUT_MS,  # Timeout (ms) khi chờ phản hồi từ server sau khi gửi truy vấn

#         waitQueueTimeoutMS=config.MONGO_WAIT_QUEUE_TIMEOUT_MS,  # Timeout (ms) khi phải chờ slot kết nối (khi pool đầy)

#         retryWrites=config.MONGO_RETRY_WRITES,  # True = tự động retry khi ghi thất bại tạm thời (mạng chập chờn)

#         tz_aware=config.MONGO_TZ_AWARE  # True = datetime trả về có timezone (hữu ích nếu xử lý thời gian toàn cầu)
        
#         # Ghi chú: journal, writeConcern không đặt ở đây,
#         # chúng được truyền khi thực hiện thao tác insert/update nếu cần độ an toàn cao.
#     )
def get_mongo_client():
    return AsyncIOMotorClient(
        config.MONGO_URI,
        maxPoolSize=config.MONGO_MAX_POOL_SIZE,
        minPoolSize=config.MONGO_MIN_POOL_SIZE,
        connectTimeoutMS=config.MONGO_CONNECT_TIMEOUT_MS,
        serverSelectionTimeoutMS=config.MONGO_SERVER_SELECTION_TIMEOUT_MS,
        socketTimeoutMS=config.MONGO_SOCKET_TIMEOUT_MS,
        waitQueueTimeoutMS=config.MONGO_WAIT_QUEUE_TIMEOUT_MS,
        retryWrites=config.MONGO_RETRY_WRITES,
        tz_aware=config.MONGO_TZ_AWARE,
        # journal và writeConcern áp dụng khi bạn ghi dữ liệu, không phải trong client constructor
    )



async def init_db():
    client = get_mongo_client()
    db = client[config.MONGO_DB]
    await init_beanie(database=db, document_models=[History])

    
# async def init_mongo():
#     client = get_mongo_client()
#     db = client[config.MONGO_DB]
#     print(f"MongoDB initialized with database: {config.MONGO_DB}")
#     return db