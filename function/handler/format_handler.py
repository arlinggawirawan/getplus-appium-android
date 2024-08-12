class FormatHandler:

    @staticmethod
    def get_email_formats():
        return [
            "gpites+@gmail",
            "gpites+qa.com",
            "gpites+qagmail.com"
        ]

    @staticmethod
    def get_phone_numbers():
        return [
            "081112345",  # Less than 10 digits
            "0811123456",  # Valid phone number with 10 digits
            "08111234567"  # Valid phone number with more than 10 digits
        ]

    @staticmethod
    def get_walkthrough_text():
        return [
            'Ada banyak cara ngumpulin poin yang bisa kamu pilih :)',
            'Bingung poin nya mau diapain?',
            'Cek merchant favorit kamu di sini :)',
            'Cek poin dan voucher kamu di sini ;)'
        ]
