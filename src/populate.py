from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Shirt, ShirtPoligon, Base

engine = create_engine("sqlite:///database.db", echo=True)

Base.metadata.create_all(bind=engine)

def populate_data():
    with Session(bind=engine) as db:

        # Define the data for each shirt
        shirts_data = [
            {
                "type": "T-SHIRT",
                "size": "P",
                "polygons": [
                {
                    "type": "frente",
                    "vertices": [
                    { "x": 0, "y": 0 },
                    { "x": 67, "y": 0 },
                    { "x": 67, "y": 67 },
                    { "x": 0, "y": 67 }
                    ]
                },
                {
                    "type": "frente",
                    "vertices": [
                    { "x": 67, "y": 0 },
                    { "x": 134, "y": 0 },
                    { "x": 134, "y": 67 },
                    { "x": 67, "y": 67 }
                    ]
                },
                {
                    "type": "costa",
                    "vertices": [
                    { "x": 134, "y": 0 },
                    { "x": 204, "y": 0 },
                    { "x": 204, "y": 70 },
                    { "x": 134, "y": 70 }
                    ]
                },
                {
                    "type": "manga",
                    "vertices": [
                    { "x": 204, "y": 0 },
                    { "x": 254, "y": 0 },
                    { "x": 254, "y": 50 },
                    { "x": 204, "y": 50 }
                    ]
                },
                {
                    "type": "manga",
                    "vertices": [
                    { "x": 254, "y": 0 },
                    { "x": 304, "y": 0 },
                    { "x": 304, "y": 50 },
                    { "x": 254, "y": 50 }
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    { "x": 346, "y": 0 },
                    { "x": 366, "y": 0 },
                    { "x": 366, "y": 20 },
                    { "x": 346, "y": 20 }
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    { "x": 366, "y": 0 },
                    { "x": 386, "y": 0 },
                    { "x": 386, "y": 20 },
                    { "x": 366, "y": 20 }
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    { "x": 386, "y": 0 },
                    { "x": 406, "y": 0 },
                    { "x": 406, "y": 20 },
                    { "x": 386, "y": 20 }
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    { "x": 406, "y": 0 },
                    { "x": 426, "y": 0 },
                    { "x": 426, "y": 20 },
                    { "x": 406, "y": 20 }
                    ]
                }
                ]
            },
            {
                "type": "T-SHIRT",
                "size": "M",
                "polygons": [
                {
                    "type": "frente",
                    "vertices": [
                    { "x": 0, "y": 70 },
                    { "x": 67, "y": 70 },
                    { "x": 67, "y": 137 },
                    { "x": 0, "y": 137 }
                    ]
                },
                {
                    "type": "frente",
                    "vertices": [
                    { "x": 67, "y": 70 },
                    { "x": 134, "y": 70 },
                    { "x": 134, "y": 137 },
                    { "x": 67, "y": 137 }
                    ]
                },
                {
                    "type": "costa",
                    "vertices": [
                    { "x": 134, "y": 70 },
                    { "x": 205, "y": 70 },
                    { "x": 205, "y": 141 },
                    { "x": 134, "y": 141 }
                    ]
                },
                {
                    "type": "manga",
                    "vertices": [
                    { "x": 205, "y": 70 },
                    { "x": 257, "y": 70 },
                    { "x": 257, "y": 122 },
                    { "x": 205, "y": 122 }
                    ]
                },
                {
                    "type": "manga",
                    "vertices": [
                    { "x": 257, "y": 70 },
                    { "x": 309, "y": 70 },
                    { "x": 309, "y": 122 },
                    { "x": 257, "y": 122 }
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    { "x": 351, "y": 70 },
                    { "x": 371, "y": 70 },
                    { "x": 371, "y": 90 },
                    { "x": 351, "y": 90 }
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    { "x": 371, "y": 70 },
                    { "x": 391, "y": 70 },
                    { "x": 391, "y": 90 },
                    { "x": 371, "y": 90 }
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    { "x": 391, "y": 70 },
                    { "x": 411, "y": 70 },
                    { "x": 411, "y": 90 },
                    { "x": 391, "y": 90 }
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    { "x": 411, "y": 70 },
                    { "x": 431, "y": 70 },
                    { "x": 431, "y": 90 },
                    { "x": 411, "y": 90 }
                    ]
                }
                ]
            },
            {
                "type": "T-SHIRT",
                "size": "G",
                "polygons": [
                {
                    "type": "frente",
                    "vertices": [
                    { "x": 0, "y": 150 },
                    { "x": 68, "y": 150 },
                    { "x": 68, "y": 218 },
                    { "x": 0, "y": 218 }
                    ]
                },
                {
                    "type": "frente",
                    "vertices": [
                    { "x": 68, "y": 150 },
                    { "x": 136, "y": 150 },
                    { "x": 136, "y": 218 },
                    { "x": 68, "y": 218 }
                    ]
                },
                {
                    "type": "costa",
                    "vertices": [
                    { "x": 136, "y": 150 },
                    { "x": 209, "y": 150 },
                    { "x": 209, "y": 223 },
                    { "x": 136, "y": 223 }
                    ]
                },
                {
                    "type": "manga",
                    "vertices": [
                    { "x": 209, "y": 150 },
                    { "x": 263, "y": 150 },
                    { "x": 263, "y": 204 },
                    { "x": 209, "y": 204 }
                    ]
                },
                {
                    "type": "manga",
                    "vertices": [
                    { "x": 263, "y": 150 },
                    { "x": 317, "y": 150 },
                    { "x": 317, "y": 204 },
                    { "x": 263, "y": 204 }
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    { "x": 359, "y": 150 },
                    { "x": 380, "y": 150 },
                    { "x": 380, "y": 171 },
                    { "x": 359, "y": 171 }
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    { "x": 380, "y": 150 },
                    { "x": 401, "y": 150 },
                    { "x": 401, "y": 171 },
                    { "x": 380, "y": 171 }
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    { "x": 401, "y": 150 },
                    { "x": 422, "y": 150 },
                    { "x": 422, "y": 171 },
                    { "x": 401, "y": 171 }
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    { "x": 422, "y": 150 },
                    { "x": 443, "y": 150 },
                    { "x": 443, "y": 171 },
                    { "x": 422, "y": 171 }
                    ]
                }
                ]
            }
        ]


        tshirt_data = [
            {
                "type": "T-SHIRT",
                "size": "P",
                "polygons": [
                {
                    "type": "frente",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 64, "y": 0},
                    {"x": 64, "y": 56},
                    {"x": 0, "y": 56}
                    ]
                },
                {
                    "type": "costa",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 70, "y": 0},
                    {"x": 70, "y": 56},
                    {"x": 0, "y": 56}
                    ]
                },
                {
                    "type": "manga",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 15, "y": 6.5},
                    {"x": 15, "y": 43.5},
                    {"x": 0, "y": 50}
                    ]
                },
                {
                    "type": "manga",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 15, "y": 6.5},
                    {"x": 15, "y": 43.5},
                    {"x": 0, "y": 50}
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 22, "y": 0},
                    {"x": 22, "y": 12},
                    {"x": 0, "y": 12}
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 22, "y": 0},
                    {"x": 22, "y": 12},
                    {"x": 0, "y": 12}
                    ]
                }
                ]
            },
            {
                "type": "T-SHIRT",
                "size": "M",
                "polygons": [
                {
                    "type": "frente",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 66, "y": 0},
                    {"x": 66, "y": 60},
                    {"x": 0, "y": 60}
                    ]
                },
                {
                    "type": "costa",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 73, "y": 0},
                    {"x": 73, "y": 60},
                    {"x": 0, "y": 60}
                    ]
                },
                {
                    "type": "manga",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 15, "y": 6.5},
                    {"x": 15, "y": 45.5},
                    {"x": 0, "y": 52}
                    ]
                },
                {
                    "type": "manga",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 15, "y": 6.5},
                    {"x": 15, "y": 45.5},
                    {"x": 0, "y": 52}
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 23, "y": 0},
                    {"x": 23, "y": 13},
                    {"x": 0, "y": 13}
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 23, "y": 0},
                    {"x": 23, "y": 13},
                    {"x": 0, "y": 13}
                    ]
                }
                ]
            },
            {
                "type": "T-SHIRT",
                "size": "G",
                "polygons": [
                {
                    "type": "frente",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 68, "y": 0},
                    {"x": 68, "y": 64},
                    {"x": 0, "y": 64}
                    ]
                },
                {
                    "type": "costa",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 76, "y": 0},
                    {"x": 76, "y": 64},
                    {"x": 0, "y": 64}
                    ]
                },
                {
                    "type": "manga",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 15, "y": 6.5},
                    {"x": 15, "y": 47.5},
                    {"x": 0, "y": 54}
                    ]
                },
                {
                    "type": "manga",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 15, "y": 6.5},
                    {"x": 15, "y": 47.5},
                    {"x": 0, "y": 54}
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                        {"x": 0, "y": 0},
                        {"x": 24, "y": 0},
                        {"x": 24, "y": 14},
                        {"x": 0, "y": 14}
                    ]
                },
                {
                    "type": "ombro",
                    "vertices": [
                    {"x": 0, "y": 0},
                    {"x": 24, "y": 0},
                    {"x": 24, "y": 14},
                    {"x": 0, "y": 14}
                    ]
                }
                ]
            }
        ]

        for shirt_data in shirts_data:

            shirt = Shirt(type=shirt_data["type"], size=shirt_data["size"])
            db.add(shirt)
            db.commit()
            db.refresh(shirt)


            for rect_data in shirt_data["polygons"]:
                rect = ShirtPoligon(vertices=rect_data["vertices"], type=rect_data["type"], shirt_id=shirt.id)
                db.add(rect)
            db.commit()
            
        for shirt_data in tshirt_data:

            shirt = Shirt(type=shirt_data["type"], size=shirt_data["size"])
            db.add(shirt)
            db.commit()
            db.refresh(shirt)


            for rect_data in shirt_data["polygons"]:
                rect = ShirtPoligon(vertices=rect_data["vertices"], type=rect_data["type"], shirt_id=shirt.id)
                db.add(rect)
            db.commit()
        # Close the database session
        db.close()


if __name__ == "__main__":
    populate_data()