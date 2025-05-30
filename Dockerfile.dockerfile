FROM python:3.11-slim

# ติดตั้ง packages ที่จำเป็น
RUN apt-get update && apt-get install -y \
    git build-essential imagemagick libgl1 \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง ssocr
RUN git clone https://github.com/jiweibo/SSOCR.git /ssocr \
    && cd /ssocr && make

# คัดลอกโค้ดของเรา
WORKDIR /app
COPY . /app

# ติดตั้ง Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
