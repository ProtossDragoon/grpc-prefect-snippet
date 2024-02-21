class PrefectException(Exception):

    def __str__(self) -> str:
        return "Prefect 실행 도중 발생한 오류입니다."
