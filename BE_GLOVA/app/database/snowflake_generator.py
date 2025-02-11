import time
import threading

class SnowflakeGenerator:
    """
    Snowflake ID 생성기
    - 64비트 ID 구성:
        1. 41비트: timestamp (밀리초 단위)
        2. 10비트: machine ID
        3. 12비트: sequence number
    """
    def __init__(self, machine_id: int, epoch: int = 1704067200000):  # 기준 epoch 설정 (2024-01-01)
        self.machine_id = machine_id & 0x3FF  # 10비트 할당
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

    def _current_timestamp(self):
        return int(time.time() * 1000)  # 밀리초 단위 타임스탬프 반환

    def __next__(self):
        with self.lock:
            timestamp = self._current_timestamp()

            # 같은 밀리초 내에서 시퀀스 증가
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & 0xFFF  # 12비트 (4096개)
                if self.sequence == 0:
                    while timestamp <= self.last_timestamp:
                        timestamp = self._current_timestamp()
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            # Snowflake ID 구성 (64비트)
            snowflake_id = ((timestamp - self.epoch) << 22) | (self.machine_id << 12) | self.sequence
            return str(snowflake_id)

# Snowflake ID 생성기 인스턴스 (machine_id는 1로 설정)
snowflake_generator = SnowflakeGenerator(machine_id=1)