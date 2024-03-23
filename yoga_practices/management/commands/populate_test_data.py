import logging

from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError

from articles.models import Article
from yoga_practices.models import Chakra, YogaPractice

logger = logging.getLogger(__name__)

MUSCLE_GROUP_NAMES = ["biceps", "neck", "calves"]
YOGA_CATEGORY_NAMES = ["beginner", "intermediate", "advanced"]
YOGA_STYLE_NAMES = ["yin", "hatha", "vinyasa"]

YOGA_POSES = [
    {
        "name": "Downward Facing Dog",
        "sanskrit_name": "Adho Mukho Svanasana",
        "description": "Donec malesuada, enim ac porta pulvinar, magna purus ultrices nisi, eget tempus mi mauris nec nibh. In pharetra id felis quis imperdiet. ",
        "chakras": [Chakra.MANIPURA, Chakra.SAHASRARA, Chakra.AJNA],
        "difficulty": 30,
        "audio_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/audio%2Fsynthesis.mp3?alt=media&token=da83cf96-57cb-42b3-9b04-861a0eb2e77b",
        "image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/poses%2F18%20Downward-Facing%20Dog.png?alt=media&token=998bcc7b-f0bd-4457-93ab-aaa0fd5b92d5",
        "duration": 22,
        "muscle_groups": [MUSCLE_GROUP_NAMES[0], MUSCLE_GROUP_NAMES[1]],
    },
    {
        "name": "Bridge Pose",
        "sanskrit_name": "Setubandha Sarvangasana",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vehicula, lectus sit amet aliquam ullamcorper, velit lacus semper risus, eget sodales diam est a ipsum.",
        "chakras": [Chakra.MANIPURA, Chakra.VISHUDDHA, Chakra.AJNA, Chakra.SAHASRARA],
        "difficulty": 20,
        "audio_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/audio%2Fsynthesis.mp3?alt=media&token=da83cf96-57cb-42b3-9b04-861a0eb2e77b",
        "image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/poses%2F06%20Bridge%20Pose.png?alt=media&token=d73015c5-620b-457c-87d1-db42ddddf346",
        "duration": 22,
        "muscle_groups": [MUSCLE_GROUP_NAMES[1], MUSCLE_GROUP_NAMES[2]],
    },
    {
        "name": "Mountain Pose",
        "sanskrit_name": "Tadasana",
        "description": "Mauris bibendum dui sit amet mauris elementum feugiat. In convallis, mi eget scelerisque consectetur, elit neque dapibus velit, nec egestas nisi elit quis tortor.",
        "chakras": [Chakra.MANIPURA, Chakra.VISHUDDHA, Chakra.AJNA, Chakra.SAHASRARA],
        "difficulty": 40,
        "audio_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/audio%2Fsynthesis.mp3?alt=media&token=da83cf96-57cb-42b3-9b04-861a0eb2e77b",
        "image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/poses%2F52%20Mountain%20Pose.png?alt=media&token=1f04b471-abc5-48e0-9548-229e29c16075",
        "duration": 22,
        "muscle_groups": [],
    },
]

YOGA_PRACTICES = [
    {
        "title": "Beginner Yin Class",
        "description": "Mauris bibendum dui sit amet mauris elementum feugiat.",
        "benefits_description": "Maecenas viverra feugiat enim vitae aliquet. Suspendisse potenti. Sed orci enim, auctor et metus id, sagittis hendrerit neque. In tempor urna in euismod aliquet. Nunc finibus nunc eget arcu condimentum facilisis eu nec eros. Cras erat odio, cursus nec orci quis, accumsan aliquam mi. Aliquam non vulputate nibh.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-oluremi-adebayo-3658399.jpg?alt=media&token=67553c24-d91a-4d1a-9df3-58b96b99c3e9",
        "style": YOGA_STYLE_NAMES[0],
        "poses": [YOGA_POSES[0], YOGA_POSES[1], YOGA_POSES[2], YOGA_POSES[1]],
    },
    {
        "title": "Morning Hatha Flow",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vehicula, lectus sit amet aliquam ullamcorper, velit lacus semper risus, eget sodales diam est a ipsum. Donec malesuada, enim ac porta pulvinar, magna purus ultrices nisi, eget tempus mi mauris nec nibh. In pharetra id felis quis imperdiet. ",
        "benefits_description": "Donec malesuada, enim ac porta pulvinar, magna purus ultrices nisi, eget tempus mi mauris nec nibh. In pharetra id felis quis imperdiet. Mauris bibendum dui sit amet mauris elementum feugiat. In convallis, mi eget scelerisque consectetur, elit neque dapibus velit, nec egestas nisi elit quis tortor.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-pixabay-355863.jpg?alt=media&token=817e4d6a-6298-4a15-8fdb-3c5cd95d7916",
        "style": YOGA_STYLE_NAMES[1],
        "poses": [YOGA_POSES[0], YOGA_POSES[1], YOGA_POSES[2], YOGA_POSES[1], YOGA_POSES[0], YOGA_POSES[1]],
    },
    {
        "title": "Quick Vinyasa Flow",
        "description": "Donec nulla orci, lobortis a dolor a, iaculis lacinia odio. Curabitur aliquam vehicula quam efficitur eleifend. Curabitur consequat ultrices dolor eu eleifend.",
        "benefits_description": "Quisque vehicula metus lectus, quis varius velit porta sit amet. Phasellus vitae aliquet felis. Nunc sagittis urna sit amet placerat fermentum.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-pnw-production-8980974%20(1).jpg?alt=media&token=41082345-7ad5-4a12-83ca-7ddbbc44e5c4",
        "style": YOGA_STYLE_NAMES[2],
        "poses": [YOGA_POSES[0], YOGA_POSES[1]],
    },
    {
        "title": "Advanced Yin",
        "description": "Aliquam sit amet nisi ut lectus gravida elementum. Nulla malesuada turpis ut sapien imperdiet tincidunt. Morbi in ante dictum, rutrum sem non, elementum purus.",
        "benefits_description": "Morbi ultrices leo id placerat iaculis. Praesent quis sapien elementum, elementum diam et, varius turpis. Aenean fermentum augue lectus, ac semper erat interdum in.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-rfstudio-3820393%20(1).jpg?alt=media&token=3640d7c6-33b1-41bb-98f6-ea9fb90ce56c",
        "style": YOGA_STYLE_NAMES[0],
        "poses": [YOGA_POSES[0], YOGA_POSES[2], YOGA_POSES[1], YOGA_POSES[0], YOGA_POSES[1]],
    },
    {
        "title": "Hatha Before Bed",
        "description": "Fusce nec ex quis enim lacinia aliquam. Cras euismod ante vitae tempus maximus. Fusce at dapibus neque. Nulla non varius nunc. Maecenas id enim vitae nibh mattis finibus. ",
        "benefits_description": "Aliquam tortor magna, rutrum ultrices tellus ac, iaculis molestie ante. Sed dui nisi, rutrum vitae sagittis eu, bibendum non purus. Maecenas imperdiet dolor magna, rhoncus tristique sem fermentum rhoncus. Vivamus nulla leo, suscipit ut ligula id, porttitor consequat metus. Praesent quis sapien elementum, elementum diam et, varius turpis. Aenean fermentum augue lectus, ac semper erat interdum in.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-rfstudio-3820393%20(1).jpg?alt=media&token=3640d7c6-33b1-41bb-98f6-ea9fb90ce56c",
        "style": YOGA_STYLE_NAMES[1],
        "poses": [
            YOGA_POSES[0],
            YOGA_POSES[1],
            YOGA_POSES[2],
            YOGA_POSES[0],
            YOGA_POSES[2],
            YOGA_POSES[1],
            YOGA_POSES[0],
        ],
    },
]

YOGA_CHALLENGES = [
    {
        "title": "Hatha for Beginners",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque posuere tellus quis consectetur suscipit. Mauris scelerisque odio felis, eget faucibus quam tincidunt ullamcorper. ",
        "benefits_description": "Curabitur augue risus, lacinia eu suscipit sed, mattis et ante. Nam vulputate, magna ac lobortis feugiat, est est elementum lorem, maximus vehicula est neque vel eros.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-rfstudio-3820393%20(1).jpg?alt=media&token=3640d7c6-33b1-41bb-98f6-ea9fb90ce56c",
        "practices": [YOGA_PRACTICES[0], YOGA_PRACTICES[2], YOGA_PRACTICES[1]],
    },
    {
        "title": "Yin Before Bed",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum efficitur lectus nec ultrices hendrerit. Interdum et malesuada fames ac ante ipsum primis in faucibus.",
        "benefits_description": "Praesent et arcu odio. Quisque imperdiet venenatis mi quis auctor. Vivamus sed nulla blandit, condimentum est eu, placerat ipsum.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-pnw-production-8980974%20(1).jpg?alt=media&token=41082345-7ad5-4a12-83ca-7ddbbc44e5c4",
        "practices": [YOGA_PRACTICES[4], YOGA_PRACTICES[1], YOGA_PRACTICES[4], YOGA_PRACTICES[2], YOGA_PRACTICES[0]],
    },
    {
        "title": "7 Days of Yoga",
        "description": "Curabitur dictum, enim id rutrum rutrum, elit lorem gravida ipsum, et iaculis nulla ipsum sed enim. Mauris non laoreet velit, at malesuada ipsum.",
        "benefits_description": "Aenean id elit non leo vehicula vehicula. Nam in scelerisque arcu. Morbi rhoncus sit amet diam at accumsan. Cras congue dui sed metus feugiat, at hendrerit sem euismod.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-oluremi-adebayo-3658399.jpg?alt=media&token=67553c24-d91a-4d1a-9df3-58b96b99c3e9",
        "practices": [
            YOGA_PRACTICES[0],
            YOGA_PRACTICES[2],
            YOGA_PRACTICES[1],
            YOGA_PRACTICES[0],
            YOGA_PRACTICES[3],
            YOGA_PRACTICES[1],
            YOGA_PRACTICES[0],
        ],
    },
    {
        "title": "Morning Yoga Program",
        "description": "Fusce nec ex quis enim lacinia aliquam. Cras euismod ante vitae tempus maximus. Fusce at dapibus neque. Nulla non varius nunc. Maecenas id enim vitae nibh mattis finibus.",
        "benefits_description": " Donec id cursus ipsum. Ut sit amet sollicitudin nulla. Praesent et nisi tincidunt, rhoncus tellus et, luctus turpis. Ut ornare velit vel tempor pellentesque.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-rfstudio-3820393%20(1).jpg?alt=media&token=3640d7c6-33b1-41bb-98f6-ea9fb90ce56c",
        "practices": [
            YOGA_PRACTICES[0],
            YOGA_PRACTICES[2],
            YOGA_PRACTICES[1],
            YOGA_PRACTICES[4],
            YOGA_PRACTICES[0],
            YOGA_PRACTICES[1],
        ],
    },
    {
        "title": "Evening Yoga Program",
        "description": "Fusce nec ex quis enim lacinia aliquam. Cras euismod ante vitae tempus maximus. Fusce at dapibus neque. Nulla non varius nunc. Maecenas id enim vitae nibh mattis finibus.",
        "benefits_description": "Donec id cursus ipsum. Ut sit amet sollicitudin nulla. Praesent et nisi tincidunt, rhoncus tellus et, luctus turpis. Ut ornare velit vel tempor pellentesque.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-oluremi-adebayo-3658399.jpg?alt=media&token=67553c24-d91a-4d1a-9df3-58b96b99c3e9",
        "practices": [
            YOGA_PRACTICES[0],
            YOGA_PRACTICES[2],
            YOGA_PRACTICES[1],
            YOGA_PRACTICES[2],
            YOGA_PRACTICES[3],
            YOGA_PRACTICES[1],
        ],
    },
]

ARTICLES = [
    {
        "title": "Benefits of Yoga",
        "content_items": [
            {
                "type": "text",
                "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque posuere tellus quis consectetur suscipit. Mauris scelerisque odio felis, eget faucibus quam tincidunt ullamcorper. Curabitur augue risus, lacinia eu suscipit sed, mattis et ante. Nam vulputate, magna ac lobortis feugiat, est est elementum lorem, maximus vehicula est neque vel eros. Pellentesque vel aliquam velit, sed pharetra ligula. Vestibulum aliquet varius consequat. Pellentesque malesuada finibus felis.",
            },
            {
                "type": "text",
                "content": "Fusce nec ex quis enim lacinia aliquam. Cras euismod ante vitae tempus maximus. Fusce at dapibus neque. Nulla non varius nunc. Maecenas id enim vitae nibh mattis finibus. Aliquam tortor magna, rutrum ultrices tellus ac, iaculis molestie ante. Sed dui nisi, rutrum vitae sagittis eu, bibendum non purus. Maecenas imperdiet dolor magna, rhoncus tristique sem fermentum rhoncus. Vivamus nulla leo, suscipit ut ligula id, porttitor consequat metus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur ultrices quis nunc varius porta. Cras et interdum nisi. Vestibulum sodales maximus gravida. Aliquam erat volutpat.",
            },
            {
                "type": "image",
                "image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-oluremi-adebayo-3658399.jpg?alt=media&token=67553c24-d91a-4d1a-9df3-58b96b99c3e9",
            },
            {
                "type": "text",
                "content": "Fusce nec ex quis enim lacinia aliquam. Cras euismod ante vitae tempus maximus. Fusce at dapibus neque. Nulla non varius nunc. Maecenas id enim vitae nibh mattis finibus. Aliquam tortor magna, rutrum ultrices tellus ac, iaculis molestie ante. Sed dui nisi, rutrum vitae sagittis eu, bibendum non purus. Maecenas imperdiet dolor magna, rhoncus tristique sem fermentum rhoncus. Vivamus nulla leo, suscipit ut ligula id, porttitor consequat metus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur ultrices quis nunc varius porta. Cras et interdum nisi. Vestibulum sodales maximus gravida. Aliquam erat volutpat.",
            },
            {
                "type": "text",
                "content": """
    •Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    •Donec pretium nunc a lectus porttitor consequat.
    •Proin auctor magna dapibus libero venenatis, non congue elit rutrum.
""",
            },
        ],
    },
    {
        "title": "What is Pranayama?",
        "content_items": [
            {
                "type": "text",
                "content": "Fusce nec ex quis enim lacinia aliquam. Cras euismod ante vitae tempus maximus. Fusce at dapibus neque. Nulla non varius nunc. Maecenas id enim vitae nibh mattis finibus. Aliquam tortor magna, rutrum ultrices tellus ac, iaculis molestie ante. Sed dui nisi, rutrum vitae sagittis eu, bibendum non purus. Maecenas imperdiet dolor magna, rhoncus tristique sem fermentum rhoncus. Vivamus nulla leo, suscipit ut ligula id, porttitor consequat metus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur ultrices quis nunc varius porta. Cras et interdum nisi. Vestibulum sodales maximus gravida. Aliquam erat volutpat.",
            },
            {
                "type": "text",
                "content": """
                •Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                •Donec pretium nunc a lectus porttitor consequat.
                •Proin auctor magna dapibus libero venenatis, non congue elit rutrum.
            """,
            },
            {
                "type": "image",
                "image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-oluremi-adebayo-3658399.jpg?alt=media&token=67553c24-d91a-4d1a-9df3-58b96b99c3e9",
            },
            {
                "type": "text",
                "content": "Mauris a eleifend eros. Sed tempor ultrices sapien at gravida. Nunc lobortis turpis nec felis suscipit iaculis. Aliquam sollicitudin felis nec lorem tincidunt venenatis. Vestibulum lobortis eros neque, eu tempor urna ultricies id. Fusce varius dolor vel mollis malesuada. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum a odio et augue hendrerit malesuada at et augue. Integer posuere urna id erat maximus, in malesuada eros pretium. Integer vehicula mollis nunc, at porttitor nulla. Vivamus quis lectus mattis, efficitur neque ut, ullamcorper augue. Integer rutrum leo at ipsum consequat fringilla. Suspendisse mollis rhoncus viverra. Aliquam augue lacus, imperdiet sed tempor ut, viverra eu ligula.",
            },
            {
                "type": "text",
                "content": "Fusce nec ex quis enim lacinia aliquam. Cras euismod ante vitae tempus maximus. Fusce at dapibus neque. Nulla non varius nunc. Maecenas id enim vitae nibh mattis finibus. Aliquam tortor magna, rutrum ultrices tellus ac, iaculis molestie ante. Sed dui nisi, rutrum vitae sagittis eu, bibendum non purus. Maecenas imperdiet dolor magna, rhoncus tristique sem fermentum rhoncus. Vivamus nulla leo, suscipit ut ligula id, porttitor consequat metus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur ultrices quis nunc varius porta. Cras et interdum nisi. Vestibulum sodales maximus gravida. Aliquam erat volutpat.",
            },
            {
                "type": "text",
                "content": "Fusce nec ex quis enim lacinia aliquam. Cras euismod ante vitae tempus maximus. Fusce at dapibus neque. Nulla non varius nunc. Maecenas id enim vitae nibh mattis finibus. Aliquam tortor magna, rutrum ultrices tellus ac, iaculis molestie ante. Sed dui nisi, rutrum vitae sagittis eu, bibendum non purus. Maecenas imperdiet dolor magna, rhoncus tristique sem fermentum rhoncus. Vivamus nulla leo, suscipit ut ligula id, porttitor consequat metus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur ultrices quis nunc varius porta. Cras et interdum nisi. Vestibulum sodales maximus gravida. Aliquam erat volutpat.",
            },
            {
                "type": "text",
                "content": "Donec tincidunt ipsum pulvinar nisi congue tempus. Aenean sit amet nisl maximus nibh suscipit congue. Vivamus dictum tellus non metus tincidunt sollicitudin. Ut dapibus velit eget felis ullamcorper eleifend. Ut nec finibus nunc. Aliquam lobortis sem in magna cursus, id ultricies sem tincidunt. Duis consequat, magna ut posuere blandit, urna justo condimentum ipsum, tempus suscipit lacus velit tincidunt felis. Etiam maximus, diam eu maximus elementum, velit augue lacinia orci, vel ornare arcu ligula a augue. Cras aliquet condimentum diam, a tempor tellus faucibus a. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nam dignissim ullamcorper lacus, id consectetur magna aliquet id. Fusce placerat tempor orci vestibulum lobortis. Pellentesque semper magna et consequat iaculis. Ut placerat odio a risus aliquet accumsan.",
            },
        ],
    },
    {
        "title": "Yoga Basics",
        "content_items": [
            {
                "type": "text",
                "content": "Donec tincidunt ipsum pulvinar nisi congue tempus. Aenean sit amet nisl maximus nibh suscipit congue. Vivamus dictum tellus non metus tincidunt sollicitudin. Ut dapibus velit eget felis ullamcorper eleifend. Ut nec finibus nunc. Aliquam lobortis sem in magna cursus, id ultricies sem tincidunt. Duis consequat, magna ut posuere blandit, urna justo condimentum ipsum, tempus suscipit lacus velit tincidunt felis. Etiam maximus, diam eu maximus elementum, velit augue lacinia orci, vel ornare arcu ligula a augue. Cras aliquet condimentum diam, a tempor tellus faucibus a. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nam dignissim ullamcorper lacus, id consectetur magna aliquet id. Fusce placerat tempor orci vestibulum lobortis. Pellentesque semper magna et consequat iaculis. Ut placerat odio a risus aliquet accumsan.",
            }
        ],
    },
    {
        "title": "Yama and Niyamas",
        "content_items": [
            {
                "type": "text",
                "content": "Donec tincidunt ipsum pulvinar nisi congue tempus. Aenean sit amet nisl maximus nibh suscipit congue. Vivamus dictum tellus non metus tincidunt sollicitudin. Ut dapibus velit eget felis ullamcorper eleifend. Ut nec finibus nunc. Aliquam lobortis sem in magna cursus, id ultricies sem tincidunt. Duis consequat, magna ut posuere blandit, urna justo condimentum ipsum, tempus suscipit lacus velit tincidunt felis. Etiam maximus, diam eu maximus elementum, velit augue lacinia orci, vel ornare arcu ligula a augue. Cras aliquet condimentum diam, a tempor tellus faucibus a. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nam dignissim ullamcorper lacus, id consectetur magna aliquet id. Fusce placerat tempor orci vestibulum lobortis. Pellentesque semper magna et consequat iaculis. Ut placerat odio a risus aliquet accumsan.",
            },
            {
                "type": "image",
                "image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-pnw-production-8980974%20(1).jpg?alt=media&token=41082345-7ad5-4a12-83ca-7ddbbc44e5c4",
            },
            {
                "type": "text",
                "content": "Donec tincidunt ipsum pulvinar nisi congue tempus. Aenean sit amet nisl maximus nibh suscipit congue. Vivamus dictum tellus non metus tincidunt sollicitudin. Ut dapibus velit eget felis ullamcorper eleifend. Ut nec finibus nunc. Aliquam lobortis sem in magna cursus, id ultricies sem tincidunt. Duis consequat, magna ut posuere blandit, urna justo condimentum ipsum, tempus suscipit lacus velit tincidunt felis. Etiam maximus, diam eu maximus elementum, velit augue lacinia orci, vel ornare arcu ligula a augue. Cras aliquet condimentum diam, a tempor tellus faucibus a. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nam dignissim ullamcorper lacus, id consectetur magna aliquet id. Fusce placerat tempor orci vestibulum lobortis. Pellentesque semper magna et consequat iaculis. Ut placerat odio a risus aliquet accumsan.",
            },
            {
                "type": "image",
                "image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-pnw-production-8980974%20(1).jpg?alt=media&token=41082345-7ad5-4a12-83ca-7ddbbc44e5c4",
            },
            {
                "type": "text",
                "content": """
                •Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                •Donec pretium nunc a lectus porttitor consequat.
                •Proin auctor magna dapibus libero venenatis, non congue elit rutrum.
            """,
            },
        ],
    },
]

YOGA_LESSONS = [
    {
        "title": "Yoga Basics",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-pnw-production-8980974%20(1).jpg?alt=media&token=41082345-7ad5-4a12-83ca-7ddbbc44e5c4",
        "priority": 0,
    },
    {
        "title": "Yama and Niyamas Explained",
        "description": "Fusce nec ex quis enim lacinia aliquam. Cras euismod ante vitae tempus maximus. Fusce at dapibus neque. Nulla non varius nunc. Maecenas id enim vitae nibh mattis finibus. Aliquam tortor magna, rutrum ultrices tellus ac, iaculis molestie ante. Sed dui nisi, rutrum vitae sagittis eu, bibendum non purus. Maecenas imperdiet dolor magna, rhoncus tristique sem fermentum rhoncus. Vivamus nulla leo, suscipit ut ligula id, porttitor consequat metus.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-pnw-production-8980974%20(1).jpg?alt=media&token=41082345-7ad5-4a12-83ca-7ddbbc44e5c4",
        "priority": 1,
    },
    {
        "title": "8 Limbs of Yoga",
        "description": "Donec pretium nunc a lectus porttitor consequat.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-oluremi-adebayo-3658399.jpg?alt=media&token=67553c24-d91a-4d1a-9df3-58b96b99c3e9",
        "priority": 2,
    },
    {
        "title": "Yoga Anatomy",
        "description": "Proin auctor magna dapibus libero venenatis, non congue elit rutrum.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-pnw-production-8980974%20(1).jpg?alt=media&token=41082345-7ad5-4a12-83ca-7ddbbc44e5c4",
        "priority": 0,
    },
    {
        "title": "Pranayama",
        "description": "Aliquam sit amet nisi ut lectus gravida elementum. Nulla malesuada turpis ut sapien imperdiet tincidunt. Morbi in ante dictum, rutrum sem non, elementum purus.",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-pnw-production-8980974%20(1).jpg?alt=media&token=41082345-7ad5-4a12-83ca-7ddbbc44e5c4",
        "priority": 1,
    },
    {
        "title": "Chakras",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque posuere tellus quis consectetur suscipit. Mauris scelerisque odio felis, eget faucibus quam tincidunt ullamcorper. ",
        "cover_image_url": "https://firebasestorage.googleapis.com/v0/b/halcyon-480af.appspot.com/o/practice-images%2Fpexels-oluremi-adebayo-3658399.jpg?alt=media&token=67553c24-d91a-4d1a-9df3-58b96b99c3e9",
        "priority": 2,
    },
]


def populate_muscle_groups():
    from yoga_practices.models import MuscleGroup

    for name in MUSCLE_GROUP_NAMES:
        try:
            MuscleGroup.objects.create(name=name)
            logger.info(f"Populated Muscle Group ({name})")
        except IntegrityError:
            pass


def populate_yoga_categories():
    from yoga_practices.models import YogaCategory

    objects = []
    for name in YOGA_CATEGORY_NAMES:
        if not YogaCategory.objects.filter(name=name).exists():
            logger.info(f"Populating Yoga Category ({name})")
            objects.append(YogaCategory(name=name, description=f"{name} - description"))
    YogaCategory.objects.bulk_create(objects)


def populate_yoga_style():
    from yoga_practices.models import YogaStyle

    objects = []
    for name in YOGA_STYLE_NAMES:
        if not YogaStyle.objects.filter(name=name).exists():
            logger.info(f"Populating Yoga Style ({name})")
            objects.append(YogaStyle(name=name, description=f"{name} - description"))
    YogaStyle.objects.bulk_create(objects)


def populate_yoga_poses():
    from yoga_practices.models import YogaPose, MuscleGroup, YogaCategory

    for pose in YOGA_POSES:
        if not YogaPose.objects.filter(name=pose["name"]).exists():
            muscle_groups = pose.pop("muscle_groups")
            obj = YogaPose.objects.create(**pose)
            for muscle_group in muscle_groups:
                obj.muscle_groups.add(MuscleGroup.objects.get(name=muscle_group))

            logger.info(f"Populated Yoga Pose ({pose['name']})")


def populate_yoga_practices():
    from yoga_practices.models import YogaPractice, YogaStyle, YogaPose, YogaPracticePose

    for practice in YOGA_PRACTICES:
        title = practice["title"]
        if not YogaPractice.objects.filter(title=title).exists():
            style_name = practice.pop("style")
            poses = practice.pop("poses")
            yoga_practice = YogaPractice.objects.create(
                created_by="Halcyon", style=YogaStyle.objects.get(name=style_name), **practice
            )
            for order, pose in enumerate(poses):
                YogaPracticePose.objects.create(
                    yoga_practice=yoga_practice, yoga_pose=YogaPose.objects.get(name=pose["name"]), order=order
                )
            logger.info(f"Populated Yoga Practice ({title})")


def populate_yoga_challenges():
    from yoga_practices.models import YogaChallenge, YogaChallengePractice, YogaPractice

    for challenge in YOGA_CHALLENGES:
        title = challenge["title"]
        if not YogaChallenge.objects.filter(title=title).exists():
            practices = challenge.pop("practices")
            yoga_challenge = YogaChallenge.objects.create(created_by="Halcyon", **challenge)
            # Populate practices
            for order, practice in enumerate(practices):
                YogaChallengePractice.objects.create(
                    yoga_challenge=yoga_challenge,
                    yoga_practice=YogaPractice.objects.get(title=practice["title"]),
                    order=order,
                )
            logger.info(f"Populated Yoga Challenge ({title})")


def create_content_item(item):
    from articles.models import ArticleImageContentItem, ArticleTextContentItem

    type = item["type"]
    if type == "image":
        return ArticleImageContentItem(**item)
    elif type == "text":
        return ArticleTextContentItem(**item)
    raise ValueError(f"Unknown item type {type}")


def populate_articles():
    from articles.models import ArticleContentItems, ArticleImageContentItem, ArticleTextContentItem

    for article in ARTICLES:
        title = article["title"]
        if Article.objects.filter(title=title).exists():
            continue
        items = []
        for item in article["content_items"]:
            items.append(create_content_item(item))
        Article.objects.create(
            title=title,
            content_items=ArticleContentItems(items=items),
        )
        logger.info(f"Populated Article ({title})")


def populate_yoga_lessons():
    from yoga_lessons.models import YogaLesson, YogaLessonArticleStep, YogaLessonPracticeStep

    for i, lesson in enumerate(YOGA_LESSONS):
        title = lesson["title"]
        if YogaLesson.objects.filter(title=title).exists():
            continue
        yoga_lesson = YogaLesson.objects.create(**lesson)
        for order in range(i + 1):
            if (i + order) % 3 == 0:
                YogaLessonArticleStep.objects.create(
                    yoga_lesson=yoga_lesson, order=order, article=Article.objects.all()[i % 4]
                )
            else:
                YogaLessonPracticeStep.objects.create(
                    yoga_lesson=yoga_lesson, order=order, yoga_practice=YogaPractice.objects.all()[i % 4]
                )

        logger.info(f"Populated Yoga Lesson ({title})")


class Command(BaseCommand):
    help = "Populates data for dev environment"

    def handle(self, *args, **options):
        if not settings.IS_DEV:
            raise Exception("This can be run only in development mode.")
        populate_muscle_groups()
        populate_yoga_categories()
        populate_yoga_style()
        populate_yoga_poses()
        populate_yoga_practices()
        populate_yoga_challenges()
        populate_articles()
        populate_yoga_lessons()
