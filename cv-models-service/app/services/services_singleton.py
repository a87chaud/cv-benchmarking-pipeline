from app.services.redis_service import RedisService
from app.services.s3_service import S3Service
from app.services.benchmarking_service import BenchMarkingService

redis_service = RedisService()
s3_service = S3Service()
benchmarking_service = BenchMarkingService()