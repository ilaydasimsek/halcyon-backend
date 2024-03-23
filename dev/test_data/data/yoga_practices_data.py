from yoga_practices.models import Chakra

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
