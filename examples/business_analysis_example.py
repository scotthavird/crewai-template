#!/usr/bin/env python
"""
Business Analysis Example - CrewAI Template
============================================

This example demonstrates how to configure CrewAI for business analysis tasks.
The crew will research market trends, analyze competition, and create strategic recommendations.

Usage (Docker):
    docker compose run --rm crew python examples/business_analysis_example.py

Or direct execution:
    python examples/business_analysis_example.py
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from datetime import datetime

from crewai_template.crew import CrewaiTemplate


def run_business_analysis():
    """
    Run a business analysis crew focused on market research and strategic planning.
    """

    # Configuration for business analysis
    inputs = {
        'topic': 'Electric Vehicle Charging Infrastructure',
        'industry': 'Automotive/Energy',
        'region': 'North America',
        'timeframe': '2024-2026',
        'current_year': str(datetime.now().year),
        'analysis_depth': 'comprehensive',
        'focus_areas': 'market size, key players, growth opportunities, regulatory landscape'
    }

    print("🚀 Starting Business Analysis Crew...")
    print(f"📊 Analyzing: {inputs['topic']}")
    print(f"🌍 Region: {inputs['region']}")
    print(f"📅 Timeframe: {inputs['timeframe']}")
    print("-" * 60)

    try:
        # Initialize and run the crew
        crew = CrewaiTemplate().crew()
        result = crew.kickoff(inputs=inputs)

        print("\n✅ Business Analysis Complete!")
        print("📄 Report saved to: report.md")

        return result

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return None

def run_competitive_analysis():
    """
    Example configuration for competitive analysis.
    """
    inputs = {
        'topic': 'AI-Powered Customer Service Platforms',
        'competitors': 'Zendesk, Salesforce Service Cloud, Intercom',
        'analysis_type': 'competitive landscape',
        'current_year': str(datetime.now().year),
        'focus_areas': 'features, pricing, market position, strengths, weaknesses'
    }

    print("🏁 Starting Competitive Analysis...")
    return CrewaiTemplate().crew().kickoff(inputs=inputs)

def run_product_research():
    """
    Example configuration for product research and development insights.
    """
    inputs = {
        'topic': 'Smart Home Security Systems',
        'research_type': 'product development',
        'target_market': 'homeowners aged 25-55',
        'current_year': str(datetime.now().year),
        'focus_areas': 'user needs, technology trends, feature requirements, pricing strategy'
    }

    print("🔬 Starting Product Research...")
    return CrewaiTemplate().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    print("🎯 CrewAI Business Analysis Examples")
    print("=" * 50)
    print("🐳 Docker Command: docker compose run --rm crew python examples/business_analysis_example.py")
    print()

    # Ask user which example to run
    print("\nSelect an analysis type:")
    print("1. Market Analysis (Electric Vehicle Charging)")
    print("2. Competitive Analysis (AI Customer Service)")
    print("3. Product Research (Smart Home Security)")
    print("4. Run all examples")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == "1":
        run_business_analysis()
    elif choice == "2":
        run_competitive_analysis()
    elif choice == "3":
        run_product_research()
    elif choice == "4":
        print("\n🚀 Running all examples...")
        run_business_analysis()
        print("\n" + "="*60)
        run_competitive_analysis()
        print("\n" + "="*60)
        run_product_research()
    else:
        print("❌ Invalid choice. Running default market analysis...")
        run_business_analysis()

    print("\n🎉 Analysis complete! Check the generated reports for insights.")
    print("💡 Next time, run with: docker compose run --rm crew python examples/business_analysis_example.py")
