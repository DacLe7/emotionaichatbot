"""
Sơ đồ mùi hương - Mapping cảm xúc với nến thơm
File này chứa logic gợi ý nến thơm dựa trên cảm xúc của người dùng
Dễ dàng tinh chỉnh và bổ sung thêm sau này
"""

class FragranceMapper:
    def __init__(self):
        # Sơ đồ mapping cảm xúc với nến thơm
        self.emotion_fragrance_map = {
            "positive": {
                "name": "Cảm xúc tích cực",
                "description": "Khi bạn cảm thấy vui vẻ, hạnh phúc, phấn khích",
                "fragrances": [
                    {
                        "name": "Nến Hương Cam Quýt Tươi Mát",
                        "scent": "Cam, Chanh, Bưởi",
                        "benefit": "Tăng năng lượng, tạo cảm giác sảng khoái",
                        "reason": "Hương cam quýt giúp tăng serotonin, hormone hạnh phúc",
                        "emoji": "🍊"
                    },
                    {
                        "name": "Nến Hương Vanilla Ngọt Ngào",
                        "scent": "Vanilla, Caramel, Gỗ Đàn Hương",
                        "benefit": "Tạo cảm giác ấm áp, thoải mái",
                        "reason": "Vanilla có tác dụng an thần, giảm stress",
                        "emoji": "🍦"
                    },
                    {
                        "name": "Nến Hương Hoa Nhài Tinh Khiết",
                        "scent": "Hoa Nhài, Hoa Hồng, Hoa Oải Hương",
                        "benefit": "Tăng cảm xúc lãng mạn, thư thái",
                        "reason": "Hoa nhài giúp cân bằng cảm xúc, tạo sự bình yên",
                        "emoji": "🌸"
                    }
                ]
            },
            "negative": {
                "name": "Cảm xúc tiêu cực",
                "description": "Khi bạn cảm thấy buồn, stress, lo lắng, mệt mỏi",
                "fragrances": [
                    {
                        "name": "Nến Hương Oải Hương Thư Giãn",
                        "scent": "Lavender, Chamomile, Bergamot",
                        "benefit": "Giảm stress, cải thiện giấc ngủ",
                        "reason": "Lavender có tác dụng an thần, giảm lo âu",
                        "emoji": "💜"
                    },
                    {
                        "name": "Nến Hương Gỗ Đàn Hương Ấm Áp",
                        "scent": "Sandalwood, Vanilla, Hương Thảo",
                        "benefit": "Tạo cảm giác bình yên, ổn định",
                        "reason": "Gỗ đàn hương giúp tĩnh tâm, giảm căng thẳng",
                        "emoji": "🪵"
                    },
                    {
                        "name": "Nến Hương Bạc Hà Tươi Mát",
                        "scent": "Peppermint, Eucalyptus, Lemon",
                        "benefit": "Tăng tập trung, giảm đau đầu",
                        "reason": "Bạc hà có tác dụng kích thích tinh thần, giảm mệt mỏi",
                        "emoji": "🌿"
                    }
                ]
            },
            "neutral": {
                "name": "Cảm xúc trung tính",
                "description": "Khi bạn cảm thấy bình thường, cân bằng",
                "fragrances": [
                    {
                        "name": "Nến Hương Hoa Cúc Dịu Nhẹ",
                        "scent": "Chamomile, Hoa Cúc, Hương Thảo",
                        "benefit": "Duy trì sự cân bằng, thư giãn nhẹ nhàng",
                        "reason": "Hoa cúc giúp duy trì trạng thái bình yên",
                        "emoji": "🌼"
                    },
                    {
                        "name": "Nến Hương Gỗ Tuyết Tùng Tự Nhiên",
                        "scent": "Cedarwood, Pine, Moss",
                        "benefit": "Kết nối với thiên nhiên, tạo cảm giác an toàn",
                        "reason": "Hương gỗ tự nhiên giúp tạo cảm giác ổn định",
                        "emoji": "🌲"
                    },
                    {
                        "name": "Nến Hương Hoa Sen Thanh Tịnh",
                        "scent": "Lotus, Bamboo, Green Tea",
                        "benefit": "Tạo không gian tĩnh lặng, thanh tịnh",
                        "reason": "Hoa sen tượng trưng cho sự bình yên và tinh khiết",
                        "emoji": "🪷"
                    }
                ]
            }
        }
    
    def get_fragrance_recommendation(self, emotion, confidence=0.5):
        """
        Lấy gợi ý nến thơm dựa trên cảm xúc
        
        Args:
            emotion (str): Cảm xúc ('positive', 'negative', 'neutral')
            confidence (float): Độ tin cậy của phân tích cảm xúc (0-1)
        
        Returns:
            dict: Thông tin gợi ý nến thơm
        """
        if emotion not in self.emotion_fragrance_map:
            # Fallback cho trường hợp không nhận diện được
            emotion = "neutral"
        
        emotion_data = self.emotion_fragrance_map[emotion]
        
        # Chọn nến thơm ngẫu nhiên từ danh sách
        import random
        selected_fragrance = random.choice(emotion_data["fragrances"])
        
        # Tạo thông điệp gợi ý
        recommendation_message = self._create_recommendation_message(
            emotion_data, selected_fragrance, confidence
        )
        
        return {
            "emotion": emotion,
            "emotion_name": emotion_data["name"],
            "emotion_description": emotion_data["description"],
            "confidence": confidence,
            "fragrance": selected_fragrance,
            "recommendation_message": recommendation_message,
            "all_fragrances": emotion_data["fragrances"]  # Tất cả lựa chọn
        }
    
    def _create_recommendation_message(self, emotion_data, fragrance, confidence):
        """Tạo thông điệp gợi ý nến thơm"""
        
        confidence_level = "rất cao" if confidence > 0.8 else "cao" if confidence > 0.6 else "trung bình"
        
        messages = {
            "positive": [
                f"Tôi thấy bạn đang cảm thấy {emotion_data['name'].lower()}! {fragrance['emoji']}",
                f"Để tăng cường cảm xúc tích cực, tôi gợi ý: **{fragrance['name']}**",
                f"💡 **Lý do**: {fragrance['reason']}",
                f"✨ **Lợi ích**: {fragrance['benefit']}",
                f"🌺 **Hương thơm**: {fragrance['scent']}"
            ],
            "negative": [
                f"Tôi hiểu bạn đang cảm thấy {emotion_data['name'].lower()}. {fragrance['emoji']}",
                f"Để cải thiện tâm trạng, tôi gợi ý: **{fragrance['name']}**",
                f"💡 **Lý do**: {fragrance['reason']}",
                f"✨ **Lợi ích**: {fragrance['benefit']}",
                f"🌺 **Hương thơm**: {fragrance['scent']}"
            ],
            "neutral": [
                f"Tôi thấy bạn đang ở trạng thái {emotion_data['name'].lower()}. {fragrance['emoji']}",
                f"Để duy trì sự cân bằng, tôi gợi ý: **{fragrance['name']}**",
                f"💡 **Lý do**: {fragrance['reason']}",
                f"✨ **Lợi ích**: {fragrance['benefit']}",
                f"🌺 **Hương thơm**: {fragrance['scent']}"
            ]
        }
        
        emotion_type = list(self.emotion_fragrance_map.keys())[
            list(self.emotion_fragrance_map.values()).index(emotion_data)
        ]
        
        return "\n".join(messages[emotion_type])
    
    def get_all_fragrances(self):
        """Lấy tất cả thông tin nến thơm"""
        return self.emotion_fragrance_map
    
    def add_fragrance(self, emotion, fragrance_data):
        """Thêm nến thơm mới (cho việc mở rộng sau này)"""
        if emotion in self.emotion_fragrance_map:
            self.emotion_fragrance_map[emotion]["fragrances"].append(fragrance_data)
            return True
        return False
    
    def update_fragrance(self, emotion, index, fragrance_data):
        """Cập nhật thông tin nến thơm (cho việc tinh chỉnh sau này)"""
        if emotion in self.emotion_fragrance_map and 0 <= index < len(self.emotion_fragrance_map[emotion]["fragrances"]):
            self.emotion_fragrance_map[emotion]["fragrances"][index] = fragrance_data
            return True
        return False

# Tạo instance mặc định
fragrance_mapper = FragranceMapper()

# Test function
def test_fragrance_mapping():
    """Test function để kiểm tra logic mapping"""
    mapper = FragranceMapper()
    
    test_emotions = ["positive", "negative", "neutral"]
    
    print("🧪 Test Fragrance Mapping")
    print("=" * 50)
    
    for emotion in test_emotions:
        print(f"\n🎭 Cảm xúc: {emotion}")
        recommendation = mapper.get_fragrance_recommendation(emotion, 0.8)
        print(f"🕯️ Gợi ý: {recommendation['fragrance']['name']}")
        print(f"🌺 Hương: {recommendation['fragrance']['scent']}")
        print(f"✨ Lợi ích: {recommendation['fragrance']['benefit']}")

if __name__ == "__main__":
    test_fragrance_mapping() 