import os
import json
import time
from datetime import datetime, timedelta
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class WeatherMonitorMockup:
    def __init__(self):
        self.schedule_history = []
        self.temperature_history = []

    def get_scheduling_context(self):
        """Provide context to AI for better scheduling decisions"""
        return {
            "recent_temperatures": self.temperature_history[-5:],  # Last 5 readings
            "recent_schedules": self.schedule_history[
                -3:
            ],  # Last 3 scheduling decisions
            "current_time": datetime.now().isoformat(),
            "day_of_week": datetime.now().strftime("%A"),
            "hour": datetime.now().hour,
        }

    def ai_schedule_decision(self, temp_data):
        """AI makes scheduling decision based on full context"""
        context = self.get_scheduling_context()

        prompt = f"""
        You are an intelligent temperature monitoring scheduler. Make a smart decision about when to check temperature next.
        
        Current temperature: {temp_data}
        Context: {json.dumps(context, indent=2)}
        
        Consider:
        - Temperature trends (is it changing rapidly?)
        - Time of day (more frequent checks during day vs night?)
        - Historical patterns
        - Energy efficiency
        
        Respond in JSON format without enclosing quotes (raw json):
        {{
            "next_check_minutes": <1-60>,
            "priority": "<low|medium|high>",
            "reason": "<explanation>",
            "adaptive_rule": "<what pattern you noticed>"
        }}
        """

        response_content = None
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            # Extract the response content
            response_content = response.choices[0].message.content
            if not response_content:
                raise ValueError("Empty response from OpenAI API")

            decision = json.loads(response_content)

            # Store decision for future context
            self.schedule_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "decision": decision,
                    "temperature": temp_data,
                }
            )

            return decision

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            if response_content:
                print(f"Raw response: {response_content}")
            return {
                "next_check_minutes": 5,
                "priority": "medium",
                "reason": "Fallback due to JSON parsing error",
                "adaptive_rule": "Error recovery",
            }
        except Exception as e:
            print(f"API call error: {e}")
            return {
                "next_check_minutes": 10,
                "priority": "low",
                "reason": "Fallback due to API error",
                "adaptive_rule": "Error recovery",
            }

    def run_monitoring(self):
        """Main monitoring loop with AI-driven scheduling"""
        print("🤖 AI Autonomous Temperature Scheduler Started!")
        print("The AI will learn and adapt its own monitoring schedule.")
        print("=" * 60)

        try:
            while True:
                # Take temperature reading
                temp_value = 20 + (time.time() % 15)  # Simulate varying temperature
                temp_data = f"{temp_value:.1f}°C"
                current_time = datetime.now().strftime("%H:%M:%S")

                # Store temperature for history
                self.temperature_history.append(
                    {"timestamp": datetime.now().isoformat(), "temperature": temp_value}
                )

                # Keep only recent history
                if len(self.temperature_history) > 20:
                    self.temperature_history = self.temperature_history[-20:]

                # Get AI's scheduling decision
                decision = self.ai_schedule_decision(temp_data)

                # Display current status
                print(f"🌡️  [{current_time}] Temperature: {temp_data}")
                print(f"🤖 AI Decision: {decision['reason']}")
                print(
                    f"⏰ Next check: {decision['next_check_minutes']} minutes ({decision['priority']} priority)"
                )
                print(f"🧠 Learning: {decision['adaptive_rule']}")
                print("-" * 60)

                # Wait according to AI's decision
                wait_seconds = decision["next_check_minutes"] * 1
                time.sleep(3)

        except KeyboardInterrupt:
            print("\n🛑 AI Scheduler stopped by user")
