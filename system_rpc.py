import time
import psutil
import pynvml
from pypresence import Presence

# Discord Developer Portalで取得したクライアントIDを入力
CLIENT_ID = "YOUR_CLIENT_ID"

# 画像のアセットキー（Developer PortalのRich Presence > Art Assetsで設定）
LARGE_IMAGE = "vibe_check_image"
LARGE_TEXT = "Vibe Check"

def get_gpu_usage():
    """NVIDIA GPUの使用率を取得する"""
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        return f"{utilization.gpu}%"
    except Exception:
        return "N/A"

def main():
    rpc = Presence(CLIENT_ID)
    rpc.connect()
    
    start_time = int(time.time())

    while True:
        try:
            # システム情報を取得
            cpu_percent = psutil.cpu_percent(interval=1)
            ram_percent = psutil.virtual_memory().percent
            gpu_percent = get_gpu_usage()
            
            # 画像のような表示形式でRPCを更新
            rpc.update(
                details=f"CPU {cpu_percent}% - GPU {gpu_percent} - RAM {ram_percent}%",
                state=" ", # 画像には2行目がないため空欄にしています
                large_image=LARGE_IMAGE,
                large_text=LARGE_TEXT,
                start=start_time
            )
            
        except Exception as e:
            print(f"エラーが発生しました: {e}")
        
        # Discordのレート制限を避けるため、15秒以上間隔を空けます
        time.sleep(15)

if __name__ == "__main__":
    main()
