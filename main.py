import streamlit as st
from abc import ABC, abstractmethod
import folium
from streamlit_folium import folium_static
import pandas as pd

# ================== REAL HOTELS DATA ==================

real_hotels = {
    "София": [
        {"name": "Grand Hotel Sofia", "stars": 5, "price": 150, "link": "https://www.grandhotelsofia.bg/", "lat": 42.6870, "lon": 23.3163, "address": "pl. "Narodno sabranie" 1"},
        {"name": "InterContinental Sofia", "stars": 5, "price": 140, "link": "https://sofia.intercontinental.com/", "lat": 42.6881, "lon": 23.3154, "address": "bul. "Narodno sabranie" 4"},
        {"name": "Hotel Marinela", "stars": 5, "price": 130, "link": "https://www.marinela.bg/", "lat": 42.6658, "lon": 23.2841, "address": "100 James Bourchier Blvd"},
        {"name": "Sofia Balkan Palace", "stars": 4, "price": 90, "link": "https://www.balkanpalaces.bg/", "lat": 42.6979, "lon": 23.3230, "address": "pl. "Sveta Nedelya" 5"},
        {"name": "Rosslyn Central Park Hotel", "stars": 4, "price": 75, "link": "https://rosslynhotels.com/", "lat": 42.6745, "lon": 23.3038, "address": "bul. "Maria Luiza" 100"},
        {"name": "Art 'Otel", "stars": 3, "price": 60, "link": "https://www.artotel.bg/", "lat": 42.6942, "lon": 23.3267, "address": "ul. "Graf Ignatiev" 5"}
    ],
    "Белград": [
        {"name": "Hyatt Regency Belgrade", "stars": 5, "price": 160, "link": "https://www.hyatt.com/", "lat": 44.8075, "lon": 20.4414, "address": "Milentija Popovića 5"},
        {"name": "Square Nine Hotel", "stars": 5, "price": 200, "link": "https://www.squareninehotel.com/", "lat": 44.8167, "lon": 20.4581, "address": "Studentski trg 9"},
        {"name": "Moskva Hotel", "stars": 4, "price": 95, "link": "https://www.hotelmoskva.rs/", "lat": 44.8106, "lon": 20.4597, "address": "Terazije 20"},
        {"name": "Falkensteiner Hotel", "stars": 4, "price": 110, "link": "https://www.falkensteiner.com/", "lat": 44.8069, "lon": 20.4242, "address": "Bulevar Mihajla Pupina 10"},
        {"name": "Hotel Prag", "stars": 3, "price": 65, "link": "http://www.hotelprag.rs/", "lat": 44.8125, "lon": 20.4608, "address": "Kraljice Natalije 27"}
    ],
    "Виена": [
        {"name": "Hotel Sacher", "stars": 5, "price": 400, "link": "https://www.sacher.com/", "lat": 48.2040, "lon": 16.3698, "address": "Philharmoniker Str. 4"},
        {"name": "Grand Hotel Wien", "stars": 5, "price": 350, "link": "https://www.grandhotelwien.com/", "lat": 48.2025, "lon": 16.3723, "address": "Kärntner Ring 9"},
        {"name": "Hilton Vienna Plaza", "stars": 5, "price": 220, "link": "https://www.hilton.com/", "lat": 48.2005, "lon": 16.3692, "address": "Schottenring 11"},
        {"name": "Hotel Kaiserhof Wien", "stars": 4, "price": 140, "link": "https://www.kaiserhof.at/", "lat": 48.2150, "lon": 16.3644, "address": "Franz-Klein-Gasse 1"},
        {"name": "Hotel Austria", "stars": 3, "price": 90, "link": "https://www.hotelaustria-wien.at/", "lat": 48.2081, "lon": 16.3765, "address": "Fleischmarkt 20"}
    ],
    "Мюнхен": [
        {"name": "Hotel Bayerischer Hof", "stars": 5, "price": 350, "link": "https://www.bayerischerhof.de/", "lat": 48.1384, "lon": 11.5729, "address": "Promenadeplatz 2-6"},
        {"name": "Mandarin Oriental Munich", "stars": 5, "price": 450, "link": "https://www.mandarinoriental.com/", "lat": 48.1369, "lon": 11.5803, "address": "Neuturmstraße 1"},
        {"name": "The Charles Hotel", "stars": 5, "price": 300, "link": "https://www.roccofortehotels.com/", "lat": 48.1489, "lon": 11.5700, "address": "Sophienstraße 28"},
        {"name": "Hotel München Palace", "stars": 4, "price": 180, "link": "https://www.muenchen-palace.de/", "lat": 48.1484, "lon": 11.5853, "address": "Trogerstraße 21"},
        {"name": "Hotel Brack", "stars": 3, "price": 110, "link": "https://www.hotel-brack.de/", "lat": 48.1388, "lon": 11.5692, "address": "Lindwurmstraße 153"}
    ]
}

# ================== DATA ==================

routes = {
    "България → Германия": ["София", "Белград", "Виена", "Мюнхен"],
    "Балкански тур": ["София", "Белград", "Букурещ", "Будапеща"],
    "Алпийски маршрут": ["Виена", "Залцбург", "Мюнхен", "Цюрих"]
}

city_info = {
    "София": {"food": ("Традиционна българска кухня", 25), "sight": "Катедралата Александър Невски", "lat": 42.6977, "lon": 23.3219},
    "Белград": {"food": ("Сръбска скара", 22), "sight": "Калемегдан", "lat": 44.7866, "lon": 20.4489},
    "Виена": {"food": ("Виенски шницел", 30), "sight": "Дворецът Шьонбрун", "lat": 48.2082, "lon": 16.3738},
    "Мюнхен": {"food": ("Немска кухня", 28), "sight": "Мариенплац", "lat": 48.1351, "lon": 11.5820},
    "Букурещ": {"food": ("Румънска кухня", 20), "sight": "Парламентът", "lat": 44.4268, "lon": 26.1025},
    "Будапеща": {"food": ("Унгарска кухня", 25), "sight": "Парламентът", "lat": 47.4979, "lon": 19.0402},
    "Залцбург": {"food": ("Австрийска кухня", 28), "sight": "Фортеца Хоензалцбург", "lat": 47.8095, "lon": 13.0550},
    "Цюрих": {"food": ("Швейцарска кухня", 35), "sight": "Езеро Цюрих", "lat": 47.3769, "lon": 8.5417}
}

DISTANCE_BETWEEN_CITIES = 300  # км

# ================== OOP ==================

class Transport(ABC):
    def __init__(self, price_per_km):
        self.price_per_km = price_per_km

    @abstractmethod
    def name(self):
        pass

    def travel_cost(self, distance):
        return distance * self.price_per_km


class Car(Transport):
    def __init__(self):
        super().__init__(0.25)

    def name(self):
        return "🚗 Кола"


class Train(Transport):
    def __init__(self):
        super().__init__(0.18)

    def name(self):
        return "🚆 Влак"


class Plane(Transport):
    def __init__(self):
        super().__init__(0.45)

    def name(self):
        return "✈️ Самолет"


# ================== FILTER HOTELS ==================

def filter_hotels_by_stars(city, min_stars):
    """Filter hotels by star rating"""
    if city in real_hotels:
        return [hotel for hotel in real_hotels[city] if hotel['stars'] >= min_stars]
    return []

# ================== CREATE MAP ==================

def create_city_map(route_cities, selected_hotels=None):
    """Create an interactive map with route and hotel markers"""
    # Center map on first city
    first_city = route_cities[0]
    city_data = city_info[first_city]
    
    m = folium.Map(
        location=[city_data['lat'], city_data['lon']],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Add route line
    route_points = []
    for city in route_cities:
        if city in city_info:
            route_points.append([city_info[city]['lat'], city_info[city]['lon']])
    
    if len(route_points) > 1:
        folium.PolyLine(
            route_points,
            color='blue',
            weight=3,
            opacity=0.7,
            popup='Маршрут'
        ).add_to(m)
    
    # Add city markers
    for city in route_cities:
        if city in city_info:
            folium.Marker(
                [city_info[city]['lat'], city_info[city]['lon']],
                popup=f"<b>{city}</b><br>{city_info[city]['sight']}",
                tooltip=city,
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
    
    # Add hotel markers if selected
    if selected_hotels:
        for hotel in selected_hotels:
            folium.Marker(
                [hotel['lat'], hotel['lon']],
                popup=f"""
                    <b>{hotel['name']}</b><br>
                    ⭐ {hotel['stars']}<br>
                    💰 {hotel['price']} лв/нощ<br>
                    📍 {hotel['address']}<br>
                    <a href="{hotel['link']}" target="_blank">🔗 Официален сайт</a>
                """,
                tooltip=hotel['name'],
                icon=folium.Icon(color='green', icon='home')
            ).add_to(m)
    
    return m

# ================== UI ==================

st.set_page_config(page_title="Туристически планер", layout="wide")

st.title("🌍 Интерактивен туристически планер")

# Sidebar for filters
with st.sidebar:
    st.header("🔍 Филтри и настройки")
    
    route_choice = st.selectbox("Избери маршрут:", list(routes.keys()))
    
    transport_choice = st.selectbox("Превозно средство:", ["Кола", "Влак", "Самолет"])
    
    # Star rating filter
    min_stars = st.slider("⭐ Минимален брой звезди на хотела:", 1, 5, 3)
    
    days = st.slider("Брой дни за путруването:", 1, 10, 4)
    
    budget = st.number_input("Твоят бюджет (лв):", 300, 10000, 1500, step=50)
    
    # Map toggle
    show_map = st.checkbox("🗺️ Покажи карта", value=True)
    show_hotels_on_map = st.checkbox("🏨 Покажи хотели на картата", value=True)

if st.button("Планирай пътуването 🧭", type="primary"):
    cities = routes[route_choice]
    
    # Избор на транспорт
    if transport_choice == "Кола":
        transport = Car()
    elif transport_choice == "Влак":
        transport = Train()
    else:
        transport = Plane()

    # Create tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Маршрут", "🏨 Хотели", "💰 Разходи", "📊 Обобщение"])

    with tab1:
        st.subheader("Маршрут")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("### 🛣️ Градове по маршрута:")
            for i, city in enumerate(cities, 1):
                st.write(f"{i}. **{city}** - {city_info[city]['sight']}")
        
        with col2:
            st.write("### 📏 Информация:")
            total_distance = DISTANCE_BETWEEN_CITIES * (len(cities) - 1)
            st.write(f"Общо разстояние: **{total_distance} км**")
            st.write(f"Превозно средство: {transport.name()}")
            st.write(f"Брой дни: **{days}**")
        
        # Display map if toggle is on
        if show_map:
            st.subheader("Интерактивна карта")
            selected_hotels_list = []
            if show_hotels_on_map:
                # Get selected hotels from first city for map display
                for city in cities[:2]:  # Show hotels from first 2 cities to avoid clutter
                    city_hotels = filter_hotels_by_stars(city, min_stars)
                    if city_hotels:
                        selected_hotels_list.append(city_hotels[0])  # Add first hotel from each city
            
            route_map = create_city_map(cities, selected_hotels_list if show_hotels_on_map else None)
            folium_static(route_map, width=700, height=400)

    with tab2:
        st.subheader("🏨 Избор на хотели")
        
        total_hotel_cost = 0
        selected_hotels = []
        
        for city in cities:
            st.markdown(f"### 📍 {city}")
            
            # Get filtered hotels for this city
            available_hotels = filter_hotels_by_stars(city, min_stars)
            
            if not available_hotels:
                st.warning(f"Няма налични хотели в {city} с минимум {min_stars} звезди")
                continue
            
            # Display hotels in columns
            cols = st.columns(len(available_hotels))
            
            for idx, hotel in enumerate(available_hotels):
                with cols[idx]:
                    st.markdown(f"**{hotel['name']}**")
                    st.write(f"⭐ {'★' * hotel['stars']}")
                    st.write(f"💰 {hotel['price']} лв/нощ")
                    
                    # Button to redirect to hotel website
                    if st.button(f"Резервирай", key=f"btn_{city}_{idx}"):
                        st.markdown(f'<meta http-equiv="refresh" content="0; url={hotel["link"]}">', unsafe_allow_html=True)
                        st.success(f"Пренасочване към {hotel['name']}...")
                    
                    st.write("---")
            
            # Calculate hotel cost (using first available hotel)
            hotel_cost = available_hotels[0]['price'] * days
            total_hotel_cost += hotel_cost
            
            # Add to selected hotels list
            selected_hotels.append({
                "city": city,
                "hotel": available_hotels[0]['name'],
                "cost": hotel_cost,
                "stars": available_hotels[0]['stars']
            })
        
        # Display selected hotels summary
        st.subheader("📋 Избрани хотели")
        hotel_df = pd.DataFrame(selected_hotels)
        if not hotel_df.empty:
            st.dataframe(
                hotel_df,
                column_config={
                    "city": "Град",
                    "hotel": "Хотел",
                    "stars": "Звезди",
                    "cost": "Цена (лв)"
                },
                hide_index=True
            )

    with tab3:
        st.subheader("💰 Детайлни разходи")
        
        # Calculate costs
        total_distance = DISTANCE_BETWEEN_CITIES * (len(cities) - 1)
        transport_cost = transport.travel_cost(total_distance)
        total_food_cost = sum(city_info[city]['food'][1] * days for city in cities)
        total_hotel_cost_calc = sum(
            filter_hotels_by_stars(city, min_stars)[0]['price'] * days 
            if filter_hotels_by_stars(city, min_stars) else 100 * days 
            for city in cities
        )
        total_cost = transport_cost + total_food_cost + total_hotel_cost_calc
        
        # Display costs in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Транспорт",
                value=f"{transport_cost:.2f} лв",
                delta=f"{transport.price_per_km} лв/км"
            )
        
        with col2:
            st.metric(
                label="Храна",
                value=f"{total_food_cost:.2f} лв",
                delta=f"{(total_food_cost/days):.1f} лв/ден"
            )
        
        with col3:
            st.metric(
                label="Хотели",
                value=f"{total_hotel_cost_calc:.2f} лв",
                delta=f"{(total_hotel_cost_calc/days):.1f} лв/ден"
            )
        
        # Progress bar for budget
        st.subheader("📊 Бюджетен анализ")
        budget_percentage = (total_cost / budget) * 100
        
        if budget_percentage > 100:
            st.error(f"Превишение с {budget_percentage-100:.1f}%")
        elif budget_percentage > 80:
            st.warning(f"Близо до лимита ({budget_percentage:.1f}%)")
        else:
            st.success(f"В рамките на бюджета ({budget_percentage:.1f}%)")
        
        st.progress(min(budget_percentage / 100, 1))
        st.write(f"**Изразходвано:** {total_cost:.2f} лв от {budget:.2f} лв")

    with tab4:
        st.subheader("📊 Обобщение на пътуването")
        
        summary_data = {
            "Параметър": ["Маршрут", "Превозно средство", "Продължителност", "Общо разстояние", 
                         "Минимални звезди", "Общ бюджет", "Общи разходи", "Статус"],
            "Стойност": [
                route_choice,
                transport.name(),
                f"{days} дни",
                f"{total_distance} км",
                f"{min_stars} ⭐",
                f"{budget:.2f} лв",
                f"{total_cost:.2f} лв",
                "✅ В рамките на бюджета" if total_cost <= budget else "❌ Над бюджета"
            ]
        }
        
        st.table(pd.DataFrame(summary_data))
        
        if total_cost <= budget:
            st.balloons()
            st.success("🎉 Бюджетът е достатъчен! Приятно пътуване! ✨")
            
            # Download itinerary button
            itinerary = f"""
            ТУРИСТИЧЕСКИ ИТИНЕРАР
            ====================
            Маршрут: {route_choice}
            Продължителност: {days} дни
            Бюджет: {budget} лв
            Общи разходи: {total_cost:.2f} лв
            
            ГРАДОВЕ:
            {chr(10).join(f'- {city}: {city_info[city]["sight"]}' for city in cities)}
            
            ХОТЕЛИ (минимум {min_stars} звезди):
            {chr(10).join(f'- {city}: {filter_hotels_by_stars(city, min_stars)[0]["name"] if filter_hotels_by_stars(city, min_stars) else "Няма налични"}' for city in cities)}
            
            РАЗХОДИ:
            - Транспорт: {transport_cost:.2f} лв
            - Храна: {total_food_cost:.2f} лв
            - Хотели: {total_hotel_cost_calc:.2f} лв
            """
            
            st.download_button(
                label="📥 Изтегли итинерара",
                data=itinerary,
                file_name="itinerary.txt",
                mime="text/plain"
            )
        else:
            st.error("❌ Бюджетът не достига. Препоръки:")
            st.write("1. Избери по-евтин транспорт")
            st.write("2. Намали броя на дните")
            st.write(f"3. Намали изискванията за хотели (сега: {min_stars} звезди)")
            st.write("4. Избери по-евтин маршрут")

# ================== INITIAL PAGE ==================
else:
    st.markdown("""
    ## 🎯 Как работи планерът?
    
    1. **Избери маршрут** от падащото меню
    2. **Избери превозно средство** (кола, влак или самолет)
    3. **Задай минимални звезди** за хотелите (1-5)
    4. **Настрой броя дни** и бюджет
    5. **Натисни "Планирай пътуването"** за да видиш детайлния план
    
    ### 🌟 Особености:
    - 🗺️ **Интерактивна карта** с маршрута и хотели
    - 🏨 **Реални хотели** с директни връзки за резервации
    - ⭐ **Филтър по звезди** за хотелите
    - 💰 **Детайлни разчети** на разходите
    - 📊 **Бюджетен анализ** с визуализация
    - 📥 **Изтегляне** на пълния итинерар
    
    *Започни като избереш маршрут от лявата страна и натиснеш бутона за планиране!*
    """)
    
    # Display sample map
    st.subheader("Примерна карта на популярни маршрути")
    sample_cities = ["София", "Белград", "Виена", "Мюнхен"]
    sample_map = create_city_map(sample_cities)
    folium_static(sample_map, width=700, height=400)
