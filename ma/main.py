from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI()

# CORS 설정 (외부 클라이언트 및 GAS와의 원활한 통신 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 클라이언트로부터 받을 데이터 구조 정의 (Pydantic 모델)
class SortRequest(BaseModel):
    data: list[int]

# 루트 경로 확인용 엔드포인트
@app.get("/")
def read_root():
    return {"status": "running", "message": "Selection Sort Cloud Run Server is active!"}

# 단순 선택 정렬 알고리즘 수행 엔드포인트
@app.post("/selection_sort")
def selection_sort(request: SortRequest):
    arr = list(request.data)
    n = len(arr)
    steps = []
    
    # 초기 상태 저장
    steps.append(list(arr))
    
    # 단순 선택 정렬 수행
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            # 최솟값 탐색
            if arr[j] < arr[min_index]:
                min_index = j
        
        # 최솟값이 현재 위치(i)가 아니라면 교환
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            steps.append(list(arr))
            
    return {
        "sorted_data": arr,
        "steps": steps,
        "complexity": "O(n^2)",
        "status": "단순 선택 정렬 완료"
    }

# Cloud Run 필수: 환경 변수 PORT를 읽어와서 서버 구동 (기본값 8080)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
