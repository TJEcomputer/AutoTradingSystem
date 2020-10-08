---
# 데이터 처리 방법
---

## 1. 날짜 데이터 형식 변환
- 증권사 API로 받은 주식데이터 중 날짜 데이터 타입을 datetime형식으로 변환 처리

```python
def transform_datetype(df):
    df['date'] = df['date'].astype('str')
    df['date'] = pd.to_datetime(df['date'])
    return df
```
## 2. Index에 날짜 데이터 반영

```python
df = df.set_index(df['date'])
```
