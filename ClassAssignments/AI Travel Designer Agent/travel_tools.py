from agents import function_tool

@function_tool
def get_flights(destination: str) -> str:
    return f"Mock flights to {destination}:\n- Airline: AirGo, Departure: 10:00 AM\n- Airline: SkyJet, Departure: 6:00 PM"

@function_tool
def suggest_hotels(destination: str) -> str:
    return f"Top hotels in {destination}:\n- Luxe Inn (5★)\n- City Comfort (4★)\n- BudgetStay (3★)"

@function_tool
def explore_city(destination: str) -> str:
    return f"Things to do in {destination}:\n- Visit historic downtown\n- Try local cuisine\n- Explore art museums"
