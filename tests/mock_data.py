class MockData():
    user1_data = {
        'uid': '12345',
        'username': 'testuser',
        'email': 'testuser@example.com'
    }
    
    trip1_data = {
        "uid": "12345",
        "trip": {
            "name": "Paris",
            "city": "Paris",
            "state": "",
            "country": "France",
            "countryAbbr": "FR",
            "lat": 48.8588897,
            "long": 2.3200410217200766,
            "imgUrl": "https://images.unsplash.com/photo-1525218291292-e46d2a90f77c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1MzAyODV8MHwxfHNlYXJjaHwxfHxQYXJpcy1JbGUtZGUtRnJhbmNlLWxhbmRtYXJrc3xlbnwwfHx8fDE3MjYyNjYzMzR8MA&ixlib=rb-4.0.3&q=80&w=1080",
            "startDate": '09/01/2024',
            "endDate": '09/05/2024'
        }
    }

    trip2_and_places_data = {
        "uid": "12345",
        "trip": {
            "name": "new trip",
            "city": "Tokyo",
            "state": "",
            "country": "Japan",
            "countryAbbr": "JP",
            "geocode": [35.6828387, 139.7594549],
            "imgUrl": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1MzAyODV8MHwxfHNlYXJjaHwxfHxUb2t5by0tbGFuZG1hcmtzfGVufDB8fHx8MTcyNjMzMDE3OHww&ixlib=rb-4.0.3&q=80&w=1080",
            "startDate": "09/15/2024",
            "endDate": "09/19/2024",
            "places": [
                {
                    "id": 1,
                    "name": "Ghibli Museum",
                    "apiId": "ChIJLYwD5TTuGGARBZKEP5BV4U0",
                    "address": "1-chōme-1-83 Shimorenjaku, Mitaka, Tokyo 181-0013, Japan",
                    "imgUrl": "https://places.googleapis.com/v1/places/ChIJLYwD5TTuGGARBZKEP5BV4U0/photos/AXCi2Q6LD18Ol_BDV0GatAqbc289S_95wWKTd-HyAUbhIgNylADNq0bdmF21KseRcRXSX96Kc-FjOmCz5us_I2U_VnOGO2kN_1MluBAzDI2C5ITvbt3r7sw3Rplg4hfmwKVgkI5zAbdNNkxYaPQSc75WyIk07maPuhH7_BjI/media?maxWidthPx=4800&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
                    "category": "Establishment",
                    "favorite": False,
                    "phoneNumber": "",
                    "rating": "4.5",
                    "summary": "Whimsical museum dedicated to the famed animation studio with a play area, theater & rooftop garden.",
                    "website": "https://www.ghibli-museum.jp/",
                    "info": "Mon: 10:00 AM – 6:00 PM, Tue: Closed, Wed: 10:00 AM – 6:00 PM, Thu: 10:00 AM – 6:00 PM, Fri: 10:00 AM – 6:00 PM, Sat: 10:00 AM – 6:00 PM, Sun: 10:00 AM – 6:00 PM",
                    "lat": 35.696238,
                    "long": 139.5704317
                },
                {
                    "id": 2,
                    "name": "Family Mart",
                    "apiId": "ChIJz52D5KKJGGARADyKkye7pxA",
                    "address": "Japan, 〒135-0061 Tokyo, Koto City, Toyosu, 5-chōme−2−１０ 沢真ビル",
                    "imgUrl": "https://places.googleapis.com/v1/places/ChIJz52D5KKJGGARADyKkye7pxA/photos/AXCi2Q4_wrKn1Z10eAUqdoyPuHRlH986jRVwSoQEneAzZX1axJtUpH3PhkGJ9CYDuafSsAF1VwITTx69S6w5j4PXvoSgBUqFh5lb-fsdAtlTxUc2kevrSobjRj8A1t1Sch9vZns7TolsjFJJ_s7ffZcZgAPge7LNjDqISu2j/media?maxWidthPx=2227&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
                    "category": "Food",
                    "favorite": False,
                    "phoneNumber": "+81 3-5547-9032",
                    "rating": "2.2",
                    "summary": "",
                    "website": "https://as.chizumaru.com/famima/detailmap?account=famima&bid=27511",
                    "info": "Mon: Open 24 hours, Tue: Open 24 hours, Wed: Open 24 hours, Thu: Open 24 hours, Fri: Open 24 hours, Sat: Open 24 hours, Sun: Open 24 hours",
                    "lat": 35.6534761,
                    "long": 139.7955297
                }
            ]
        }
    }

    trip3_and_places_data = {
        "uid": "12345",
        "trip": {
            "name": "new trip",
            "city": "Tokyo",
            "state": "",
            "country": "Japan",
            "countryAbbr": "JP",
            "geocode": [35.6828387, 139.7594549],
            "imgUrl": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1MzAyODV8MHwxfHNlYXJjaHwxfHxUb2t5by0tbGFuZG1hcmtzfGVufDB8fHx8MTcyNjMzMDE3OHww&ixlib=rb-4.0.3&q=80&w=1080",
            "startDate": "09/15/2024",
            "endDate": "09/17/2024",
            "places": [
                {
                    "id": 1,
                    "name": "Ghibli Museum",
                    "apiId": "ChIJLYwD5TTuGGARBZKEP5BV4U0",
                    "address": "1-chōme-1-83 Shimorenjaku, Mitaka, Tokyo 181-0013, Japan",
                    "imgUrl": "https://places.googleapis.com/v1/places/ChIJLYwD5TTuGGARBZKEP5BV4U0/photos/AXCi2Q6LD18Ol_BDV0GatAqbc289S_95wWKTd-HyAUbhIgNylADNq0bdmF21KseRcRXSX96Kc-FjOmCz5us_I2U_VnOGO2kN_1MluBAzDI2C5ITvbt3r7sw3Rplg4hfmwKVgkI5zAbdNNkxYaPQSc75WyIk07maPuhH7_BjI/media?maxWidthPx=4800&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
                    "category": "Establishment",
                    "favorite": False,
                    "phoneNumber": "",
                    "rating": "4.5",
                    "summary": "Whimsical museum dedicated to the famed animation studio with a play area, theater & rooftop garden.",
                    "website": "https://www.ghibli-museum.jp/",
                    "info": "Mon: 10:00 AM – 6:00 PM, Tue: Closed, Wed: 10:00 AM – 6:00 PM, Thu: 10:00 AM – 6:00 PM, Fri: 10:00 AM – 6:00 PM, Sat: 10:00 AM – 6:00 PM, Sun: 10:00 AM – 6:00 PM",
                    "lat": 35.696238,
                    "long": 139.5704317
                },
                {
                    "id": 2,
                    "name": "Family Mart",
                    "apiId": "ChIJz52D5KKJGGARADyKkye7pxA",
                    "address": "Japan, 〒135-0061 Tokyo, Koto City, Toyosu, 5-chōme−2−１０ 沢真ビル",
                    "imgUrl": "https://places.googleapis.com/v1/places/ChIJz52D5KKJGGARADyKkye7pxA/photos/AXCi2Q4_wrKn1Z10eAUqdoyPuHRlH986jRVwSoQEneAzZX1axJtUpH3PhkGJ9CYDuafSsAF1VwITTx69S6w5j4PXvoSgBUqFh5lb-fsdAtlTxUc2kevrSobjRj8A1t1Sch9vZns7TolsjFJJ_s7ffZcZgAPge7LNjDqISu2j/media?maxWidthPx=2227&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
                    "category": "Food",
                    "favorite": False,
                    "phoneNumber": "+81 3-5547-9032",
                    "rating": "2.2",
                    "summary": "",
                    "website": "https://as.chizumaru.com/famima/detailmap?account=famima&bid=27511",
                    "info": "Mon: Open 24 hours, Tue: Open 24 hours, Wed: Open 24 hours, Thu: Open 24 hours, Fri: Open 24 hours, Sat: Open 24 hours, Sun: Open 24 hours",
                    "lat": 35.6534761,
                    "long": 139.7955297
                },
                {
                    "id": 3,
                    "name": "cherry blossom",
                    "apiId": "ChIJ39GHSE71GGARnwBli1-HcHM",
                    "address": "Japan, 〒211-0063 Kanagawa, Kawasaki, Nakahara Ward, Kosugimachi, 1-chōme−５２６−１７, Akiba Bld., 1階",
                    "imgUrl": "https://places.googleapis.com/v1/places/ChIJ39GHSE71GGARnwBli1-HcHM/photos/AXCi2Q4K8EV0ZBGj1TbQVZBg0N744CgDOFGHjdQnqyLFyO3S6obRhNgl_4HpixJtkey0THktUxI34OaGAWrQFWwxemqLoYSpdWJR8Phu4fC0YJpxrM3xN9Xmt7W9UoPgprwy-oTJ29z-RrdQkaFlGVpgO_o1JFPGJVocyTHl/media?maxWidthPx=1387&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
                    "category": "Restaurant",
                    "favorite": False,
                    "phoneNumber": "+81 50-5462-3014",
                    "rating": "4.4",
                    "summary": "",
                    "website": "https://cherryblossom.foodre.jp/",
                    "info": "Mon: 5:00 – 10:00 PM, Tue: 11:30 AM – 2:00 PM; 5:00 PM – 12:00 AM, Wed: 11:30 AM – 2:00 PM; 5:00 PM – 12:00 AM, Thu: 11:30 AM – 2:00 PM; 5:00 PM – 12:00 AM, Fri: 5:00 PM – 12:00 AM, Sat: 5:00 PM – 12:00 AM, Sun: 5:00 – 10:00 PM",
                    "lat": 35.5783884,
                    "long": 139.65884269999998
                },
                {
                    "id": 4,
                    "name": "Imperial Palace",
                    "apiId": "ChIJTQbYAg2MGGARt22eNwtfGtE",
                    "address": "1-1 Chiyoda, Chiyoda City, Tokyo 100-8111, Japan",
                    "imgUrl": "https://places.googleapis.com/v1/places/ChIJTQbYAg2MGGARt22eNwtfGtE/photos/AXCi2Q6Tdn8XNxGbQXJPw38re-_ESgq6KoCKX_7dJtgsc93PLEXPCjWZ1HKbQO7F2Z0BBeMc3s1hbWsK5IjXdYjhZl_LXZyNVRsRCvA5Fs6zYbuF_Dyll28s5FoXOTcmPi_x6LV1miCrw10TneAWURiinZnTy69rzKLoHiF-/media?maxWidthPx=728&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
                    "category": "Park",
                    "favorite": False,
                    "phoneNumber": "+81 3-3213-1111",
                    "rating": "4.4",
                    "summary": "This site with scenic gardens & tours of the grounds is the main residence of the emperor of Japan.",
                    "website": "https://sankan.kunaicho.go.jp/index.html",
                    "info": "Mon: Closed, Tue: 9:00 – 11:15 AM; 1:30 – 2:45 PM, Wed: 9:00 – 11:15 AM; 1:30 – 2:45 PM, Thu: 9:00 – 11:15 AM; 1:30 – 2:45 PM, Fri: 9:00 – 11:15 AM; 1:30 – 2:45 PM, Sat: 9:00 – 11:15 AM; 1:30 – 2:45 PM, Sun: Closed",
                    "lat": 35.685175,
                    "long": 139.75279949999998
                },
                {
                    "id": 5,
                    "name": "KANDA SQUARE HALL",
                    "apiId": "ChIJDVeyP06NGGARrb6m8OewxpM",
                    "address": "Japan, 〒101-0054 Tokyo, Chiyoda City, Kanda Nishikichō, 2-chōme−２−１",
                    "imgUrl": "https://places.googleapis.com/v1/places/ChIJDVeyP06NGGARrb6m8OewxpM/photos/AXCi2Q7L5q8I0WPY7OZR120cO201QCHPyp4EukEKwDeVSSbCEqUQ-Z3XyKftSN2bxlrIhkEdMHsYvRauc8lV2IDkvmT1rRV8A9a8ZFhFKgdOizBrlMFjS5EGViw4DWP2id6dXlrvPngAFS02fAnE82GvSYy9VqZlsmm3kdPi/media?maxWidthPx=1772&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
                    "category": "Store",
                    "favorite": False,
                    "phoneNumber": "",
                    "rating": "4.0",
                    "summary": "",
                    "website": "https://kanda-square.com/hall/",
                    "info": "",
                    "lat": 35.6931252,
                    "long": 139.7632042
                }
            ]
        }
    }

    place1_data = {
        "name": "Mikokuyu",
        "apiId": "ChIJm7-AtNKOGGARhV1nBG9UDtM",
        "address": "3-chōme-30-10 Ishiwara, Sumida City, Tokyo 130-0011, Japan",
        "imgUrl": "https://places.googleapis.com/v1/places/ChIJm7-AtNKOGGARhV1nBG9UDtM/photos/AXCi2Q57z0yB95SeaVMq3CrdQxQ3fWzy4JzlxwbJgNZQ1-Klx2vxTcpYL0y9xthW3czVdYFUaR2CSPYrUD9eMutlXbTZb-l7axjCP3uEuW5tiPIYYVx5nY0ce9Jp4MoJeyBkQFroqYJXuFP_LhlZwr0wCBRC8o9zvkoGqroz/media?maxWidthPx=4032&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
        "category": "Establishment",
        "favorite": False,
        "phoneNumber": "+81 3-3623-1695",
        "rating": "4.3",
        "summary": "Baths with 2 floors of pools at varying temperatures, including a pool with views of the Skytree.",
        "website": "http://mikokuyu.com/",
        "info": "Mon: Closed, Tue: 3:30 PM – 2:00 AM, Wed: 3:30 PM – 2:00 AM, Thu: 3:30 PM – 2:00 AM, Fri: 3:30 PM – 2:00 AM, Sat: 3:30 PM – 2:00 AM, Sun: 3:00 PM – 12:00 AM",
        "lat": 35.701527,
        "long": 139.804531
    }

    place2_data = {
        "name": "Ghibli Museum",
        "apiId": "ChIJLYwD5TTuGGARBZKEP5BV4U0",
        "address": "1-chōme-1-83 Shimorenjaku, Mitaka, Tokyo 181-0013, Japan",
        "imgUrl": "https://places.googleapis.com/v1/places/ChIJLYwD5TTuGGARBZKEP5BV4U0/photos/AXCi2Q6LD18Ol_BDV0GatAqbc289S_95wWKTd-HyAUbhIgNylADNq0bdmF21KseRcRXSX96Kc-FjOmCz5us_I2U_VnOGO2kN_1MluBAzDI2C5ITvbt3r7sw3Rplg4hfmwKVgkI5zAbdNNkxYaPQSc75WyIk07maPuhH7_BjI/media?maxWidthPx=4800&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
        "category": "Establishment",
        "favorite": False,
        "phoneNumber": "",
        "rating": "4.5",
        "summary": "Whimsical museum dedicated to the famed animation studio with a play area, theater & rooftop garden.",
        "website": "https://www.ghibli-museum.jp/",
        "info": "Mon: 10:00 AM – 6:00 PM, Tue: Closed, Wed: 10:00 AM – 6:00 PM, Thu: 10:00 AM – 6:00 PM, Fri: 10:00 AM – 6:00 PM, Sat: 10:00 AM – 6:00 PM, Sun: 10:00 AM – 6:00 PM",
        "lat": 35.696238,
        "long": 139.5704317
    }

    place3_data = {
        "name": "KANDA SQUARE HALL",
        "apiId": "ChIJDVeyP06NGGARrb6m8OewxpM",
        "address": "Japan, 〒101-0054 Tokyo, Chiyoda City, Kanda Nishikichō, 2-chōme−２−１",
        "imgUrl": "https://places.googleapis.com/v1/places/ChIJDVeyP06NGGARrb6m8OewxpM/photos/AXCi2Q7L5q8I0WPY7OZR120cO201QCHPyp4EukEKwDeVSSbCEqUQ-Z3XyKftSN2bxlrIhkEdMHsYvRauc8lV2IDkvmT1rRV8A9a8ZFhFKgdOizBrlMFjS5EGViw4DWP2id6dXlrvPngAFS02fAnE82GvSYy9VqZlsmm3kdPi/media?maxWidthPx=1772&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
        "category": "Store",
        "favorite": False,
        "phoneNumber": "",
        "rating": "4.0",
        "summary": "",
        "website": "https://kanda-square.com/hall/",
        "info": "",
        "lat": 35.6931252,
        "long": 139.7632042
    }

    place4_data = {
        "name": "Family Mart",
        "apiId": "ChIJz52D5KKJGGARADyKkye7pxA",
        "address": "Japan, 〒135-0061 Tokyo, Koto City, Toyosu, 5-chōme−2−１０ 沢真ビル",
        "imgUrl": "https://places.googleapis.com/v1/places/ChIJz52D5KKJGGARADyKkye7pxA/photos/AXCi2Q4_wrKn1Z10eAUqdoyPuHRlH986jRVwSoQEneAzZX1axJtUpH3PhkGJ9CYDuafSsAF1VwITTx69S6w5j4PXvoSgBUqFh5lb-fsdAtlTxUc2kevrSobjRj8A1t1Sch9vZns7TolsjFJJ_s7ffZcZgAPge7LNjDqISu2j/media?maxWidthPx=2227&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
        "category": "Food",
        "favorite": False,
        "phoneNumber": "+81 3-5547-9032",
        "rating": "2.2",
        "summary": "",
        "website": "https://as.chizumaru.com/famima/detailmap?account=famima&bid=27511",
        "info": "Mon: Open 24 hours, Tue: Open 24 hours, Wed: Open 24 hours, Thu: Open 24 hours, Fri: Open 24 hours, Sat: Open 24 hours, Sun: Open 24 hours",
        "lat": 35.6534761,
        "long": 139.7955297
    }

    place5_data = {
        "name": "Imperial Palace",
        "apiId": "ChIJTQbYAg2MGGARt22eNwtfGtE",
        "address": "1-1 Chiyoda, Chiyoda City, Tokyo 100-8111, Japan",
        "imgUrl": "https://places.googleapis.com/v1/places/ChIJTQbYAg2MGGARt22eNwtfGtE/photos/AXCi2Q6Tdn8XNxGbQXJPw38re-_ESgq6KoCKX_7dJtgsc93PLEXPCjWZ1HKbQO7F2Z0BBeMc3s1hbWsK5IjXdYjhZl_LXZyNVRsRCvA5Fs6zYbuF_Dyll28s5FoXOTcmPi_x6LV1miCrw10TneAWURiinZnTy69rzKLoHiF-/media?maxWidthPx=728&key=AIzaSyDSb_2EDA9dG4bMW6QtRcTrqHy3MkLmxPU",
        "category": "Park",
        "favorite": False,
        "phoneNumber": "+81 3-3213-1111",
        "rating": "4.4",
        "summary": "This site with scenic gardens & tours of the grounds is the main residence of the emperor of Japan.",
        "website": "https://sankan.kunaicho.go.jp/index.html",
        "info": "Mon: Closed, Tue: 9:00 – 11:15 AM; 1:30 – 2:45 PM, Wed: 9:00 – 11:15 AM; 1:30 – 2:45 PM, Thu: 9:00 – 11:15 AM; 1:30 – 2:45 PM, Fri: 9:00 – 11:15 AM; 1:30 – 2:45 PM, Sat: 9:00 – 11:15 AM; 1:30 – 2:45 PM, Sun: Closed",
        "lat": 35.685175,
        "long": 139.75279949999998
    }