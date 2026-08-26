from core.image_generation import generate_future_city_image


image = generate_future_city_image(
    country="Algeria",
    city="Oran",
    problem="Water Scarcity",
    solution="Smart Water Management",
    sector="Water Infrastructure",
    projected_effects=[
        "Improved water availability",
        "Reduced water losses",
        "More efficient urban water infrastructure",
        "Greater resilience to drought"
    ]
)

image.save("test_future_city.png")

print("IMAGE_GENERATED_SUCCESSFULLY")