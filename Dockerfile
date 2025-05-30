FROM python:3.11-slim

# ติดตั้ง dependencies ระบบ
RUN apt-get update && apt-get install -y \
    git build-essential imagemagick libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Clone ssocr
RUN git clone https://github.com/jiweibo/SSOCR.git /ssocr && \
    cd /ssocr && make

# ตั้ง working directory และคัดลอกไฟล์ทั้งหมด
WORKDIR /app
COPY . /app

# ติดตั้ง Python packages
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
