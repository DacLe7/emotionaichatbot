from db.postgres_database import PostgresDatabase

if __name__ == "__main__":
    db = PostgresDatabase()
    # Ví dụ thêm fragrance mới
    new_fragrance = db.add_fragrance(
        name="Nến Hương Hoa Hồng Lãng Mạn",
        description="Tạo cảm giác lãng mạn, thư thái cho không gian sống",
        emotion="positive",
        image_url="https://link-to-image.com/rose-candle.jpg"
    )
    print("Đã thêm fragrance mới:", new_fragrance)
    db.close() 