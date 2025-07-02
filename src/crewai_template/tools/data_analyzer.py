import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class DataAnalyzerInput(BaseModel):
    """Input schema for DataAnalyzerTool."""
    data: str = Field(..., description="Data to analyze (JSON, CSV format, or structured text)")
    analysis_type: str = Field(
        default="summary",
        description="Type of analysis: 'summary', 'trends', 'patterns', 'statistics', or 'insights'"
    )
    focus_area: Optional[str] = Field(
        default=None,
        description="Specific area to focus the analysis on"
    )

class DataAnalyzerTool(BaseTool):
    name: str = "Advanced Data Analyzer"
    description: str = (
        "Analyzes structured and unstructured data to extract insights, identify patterns, "
        "and generate statistical summaries. Supports multiple analysis types including "
        "trend analysis, pattern recognition, and comprehensive data insights."
    )
    args_schema: Type[BaseModel] = DataAnalyzerInput

    def _run(self, data: str, analysis_type: str = "summary", focus_area: Optional[str] = None) -> str:
        """
        Analyze data and return insights based on the specified analysis type.

        Args:
            data: The data to analyze (JSON, CSV, or structured text)
            analysis_type: Type of analysis to perform
            focus_area: Specific area to focus on

        Returns:
            Formatted analysis results with insights and recommendations
        """
        try:
            logger.info(f"Starting {analysis_type} analysis on data")

            # Parse the data
            parsed_data = self._parse_data(data)

            # Perform analysis based on type
            if analysis_type == "summary":
                result = self._generate_summary(parsed_data, focus_area)
            elif analysis_type == "trends":
                result = self._analyze_trends(parsed_data, focus_area)
            elif analysis_type == "patterns":
                result = self._identify_patterns(parsed_data, focus_area)
            elif analysis_type == "statistics":
                result = self._calculate_statistics(parsed_data, focus_area)
            elif analysis_type == "insights":
                result = self._extract_insights(parsed_data, focus_area)
            else:
                result = self._generate_summary(parsed_data, focus_area)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            return f"""
📊 Data Analysis Report
Generated: {timestamp}
Analysis Type: {analysis_type.title()}
Focus Area: {focus_area or 'General'}

{result}

---
💡 Tip: Try different analysis types (summary, trends, patterns, statistics, insights) for deeper understanding.
"""

        except Exception as e:
            error_msg = f"Error analyzing data: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def _parse_data(self, data: str) -> Dict[str, Any]:
        """Parse input data into a structured format."""
        try:
            # Try parsing as JSON first
            return {"type": "json", "content": json.loads(data)}
        except json.JSONDecodeError:
            # Try parsing as CSV-like data
            lines = data.strip().split('\n')
            if len(lines) > 1 and (',' in lines[0] or '\t' in lines[0]):
                separator = ',' if ',' in lines[0] else '\t'
                headers = [h.strip() for h in lines[0].split(separator)]
                rows = []
                for line in lines[1:]:
                    if line.strip():
                        rows.append([cell.strip() for cell in line.split(separator)])
                return {"type": "table", "headers": headers, "rows": rows}
            else:
                # Treat as unstructured text
                return {"type": "text", "content": data}

    def _generate_summary(self, data: Dict[str, Any], focus_area: Optional[str]) -> str:
        """Generate a comprehensive summary of the data."""
        if data["type"] == "json":
            content = data["content"]
            summary = f"📋 Data Summary:\n"
            summary += f"• Data Type: JSON with {len(content)} top-level items\n"

            if isinstance(content, dict):
                summary += f"• Keys: {', '.join(list(content.keys())[:5])}\n"
                if len(content) > 5:
                    summary += f"• ... and {len(content) - 5} more keys\n"
            elif isinstance(content, list):
                summary += f"• List with {len(content)} items\n"
                if content and isinstance(content[0], dict):
                    summary += f"• Sample keys: {', '.join(list(content[0].keys())[:3])}\n"

        elif data["type"] == "table":
            headers = data["headers"]
            rows = data["rows"]
            summary = f"📊 Table Summary:\n"
            summary += f"• Columns: {len(headers)} ({', '.join(headers[:3])}{'...' if len(headers) > 3 else ''})\n"
            summary += f"• Rows: {len(rows)}\n"
            summary += f"• Total Data Points: {len(headers) * len(rows)}\n"

        else:
            content = data["content"]
            word_count = len(content.split())
            line_count = len(content.split('\n'))
            summary = f"📝 Text Summary:\n"
            summary += f"• Word Count: {word_count}\n"
            summary += f"• Line Count: {line_count}\n"
            summary += f"• Character Count: {len(content)}\n"

        if focus_area:
            summary += f"\n🎯 Focus Area Analysis: {focus_area}\n"
            summary += self._analyze_focus_area(data, focus_area)

        return summary

    def _analyze_trends(self, data: Dict[str, Any], focus_area: Optional[str]) -> str:
        """Analyze trends in the data."""
        trends = "📈 Trend Analysis:\n\n"

        if data["type"] == "table":
            headers = data["headers"]
            rows = data["rows"]

            # Look for numeric columns
            numeric_cols = []
            for i, header in enumerate(headers):
                try:
                    # Check if most values in this column are numeric
                    numeric_count = 0
                    for row in rows[:10]:  # Sample first 10 rows
                        if i < len(row):
                            try:
                                float(row[i])
                                numeric_count += 1
                            except ValueError:
                                pass
                    if numeric_count > len(rows[:10]) * 0.5:  # More than 50% numeric
                        numeric_cols.append((i, header))
                except:
                    pass

            if numeric_cols:
                trends += f"• Found {len(numeric_cols)} numeric columns for trend analysis\n"
                for col_idx, col_name in numeric_cols[:3]:
                    values = []
                    for row in rows:
                        if col_idx < len(row):
                            try:
                                values.append(float(row[col_idx]))
                            except ValueError:
                                pass

                    if len(values) > 1:
                        if values[-1] > values[0]:
                            trend_direction = "📈 Increasing"
                        elif values[-1] < values[0]:
                            trend_direction = "📉 Decreasing"
                        else:
                            trend_direction = "➡️ Stable"

                        trends += f"• {col_name}: {trend_direction} (from {values[0]:.2f} to {values[-1]:.2f})\n"
            else:
                trends += "• No clear numeric trends detected in the data\n"

        elif data["type"] == "text":
            # Analyze text trends (word frequency, sentiment indicators)
            content = data["content"].lower()
            words = re.findall(r'\b\w+\b', content)
            word_freq = {}
            for word in words:
                if len(word) > 3:  # Focus on meaningful words
                    word_freq[word] = word_freq.get(word, 0) + 1

            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            trends += "• Top trending words:\n"
            for word, count in top_words:
                trends += f"  - {word}: {count} occurrences\n"

        return trends

    def _identify_patterns(self, data: Dict[str, Any], focus_area: Optional[str]) -> str:
        """Identify patterns in the data."""
        patterns = "🔍 Pattern Analysis:\n\n"

        if data["type"] == "table":
            headers = data["headers"]
            rows = data["rows"]

            # Look for patterns in categorical data
            for col_idx, header in enumerate(headers):
                values = []
                for row in rows:
                    if col_idx < len(row) and row[col_idx]:
                        values.append(row[col_idx])

                if values:
                    unique_values = list(set(values))
                    if len(unique_values) < len(values) * 0.8:  # Some repetition
                        value_counts = {}
                        for val in values:
                            value_counts[val] = value_counts.get(val, 0) + 1

                        most_common = max(value_counts.items(), key=lambda x: x[1])
                        patterns += f"• {header}: Most common value is '{most_common[0]}' ({most_common[1]} times)\n"

        elif data["type"] == "text":
            content = data["content"]

            # Look for repeated phrases
            sentences = re.split(r'[.!?]+', content)
            if len(sentences) > 1:
                patterns += f"• Text structure: {len(sentences)} sentences detected\n"

            # Look for common patterns
            if re.search(r'\d{4}-\d{2}-\d{2}', content):
                patterns += "• Contains date patterns (YYYY-MM-DD format)\n"
            if re.search(r'\b\d+%\b', content):
                patterns += "• Contains percentage values\n"
            if re.search(r'\$\d+', content):
                patterns += "• Contains currency values\n"

        return patterns

    def _calculate_statistics(self, data: Dict[str, Any], focus_area: Optional[str]) -> str:
        """Calculate basic statistics for numeric data."""
        stats = "📊 Statistical Analysis:\n\n"

        if data["type"] == "table":
            headers = data["headers"]
            rows = data["rows"]

            for col_idx, header in enumerate(headers):
                values = []
                for row in rows:
                    if col_idx < len(row):
                        try:
                            values.append(float(row[col_idx]))
                        except ValueError:
                            pass

                if len(values) > 0:
                    avg = sum(values) / len(values)
                    min_val = min(values)
                    max_val = max(values)

                    stats += f"• {header}:\n"
                    stats += f"  - Average: {avg:.2f}\n"
                    stats += f"  - Range: {min_val:.2f} to {max_val:.2f}\n"
                    stats += f"  - Count: {len(values)} values\n\n"

        elif data["type"] == "text":
            content = data["content"]
            words = content.split()
            sentences = re.split(r'[.!?]+', content)

            stats += f"• Text Statistics:\n"
            stats += f"  - Words: {len(words)}\n"
            stats += f"  - Sentences: {len([s for s in sentences if s.strip()])}\n"
            stats += f"  - Avg words per sentence: {len(words) / max(len(sentences), 1):.1f}\n"
            stats += f"  - Characters: {len(content)}\n"

        return stats

    def _extract_insights(self, data: Dict[str, Any], focus_area: Optional[str]) -> str:
        """Extract actionable insights from the data."""
        insights = "💡 Key Insights & Recommendations:\n\n"

        # Combine multiple analysis types for comprehensive insights
        summary = self._generate_summary(data, focus_area)
        trends = self._analyze_trends(data, focus_area)
        patterns = self._identify_patterns(data, focus_area)

        insights += "🔍 Data Overview:\n"
        if data["type"] == "table":
            insights += f"• Structured dataset with {len(data['rows'])} records\n"
            insights += f"• {len(data['headers'])} attributes available for analysis\n"
        elif data["type"] == "json":
            insights += "• JSON data structure detected - good for API integration\n"
        else:
            insights += "• Unstructured text data - suitable for NLP analysis\n"

        insights += "\n🎯 Actionable Recommendations:\n"
        insights += "• Consider visualizing numeric trends with charts\n"
        insights += "• Look for correlations between different data points\n"
        insights += "• Validate data quality and handle missing values\n"

        if focus_area:
            insights += f"• Deep dive into {focus_area} for specialized insights\n"

        return insights

    def _analyze_focus_area(self, data: Dict[str, Any], focus_area: str) -> str:
        """Analyze data with specific focus on a particular area."""
        focus_analysis = ""
        focus_lower = focus_area.lower()

        if data["type"] == "text":
            content = data["content"].lower()
            if focus_lower in content:
                # Count mentions and extract context
                mentions = content.count(focus_lower)
                focus_analysis += f"• '{focus_area}' mentioned {mentions} times in the text\n"

                # Extract sentences containing the focus area
                sentences = re.split(r'[.!?]+', data["content"])
                relevant_sentences = [s.strip() for s in sentences if focus_lower in s.lower()][:3]
                if relevant_sentences:
                    focus_analysis += "• Relevant context:\n"
                    for sentence in relevant_sentences:
                        focus_analysis += f"  - {sentence[:100]}...\n"

        elif data["type"] == "table":
            headers = data["headers"]
            # Look for columns related to focus area
            relevant_cols = [h for h in headers if focus_lower in h.lower()]
            if relevant_cols:
                focus_analysis += f"• Found relevant columns: {', '.join(relevant_cols)}\n"

        return focus_analysis
