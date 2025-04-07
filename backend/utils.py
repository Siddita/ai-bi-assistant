import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import io
import base64
import logging
from sqlalchemy import text

logger = logging.getLogger(__name__)

def generate_sql_query(question: str) -> text:
    # This is a simplified version - in production, you'd use OpenAI to generate the SQL
    if "sales" in question.lower():
        return text("SELECT * FROM sales")
    elif "products" in question.lower():
        return text("SELECT * FROM products")
    elif "customers" in question.lower():
        return text("SELECT * FROM customers")
    else:
        return text("SELECT * FROM sales")

async def generate_visualization(df: pd.DataFrame) -> dict:
    try:
        plt.figure(figsize=(10, 6))
        if 'total_amount' in df.columns:
            df.plot(x='sale_date', y='total_amount', kind='line')
        else:
            df.plot(kind='bar')
        
        plt.title('Data Visualization')
        plt.xlabel('Date')
        plt.ylabel('Value')
        
        # Save plot to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        plt.close()
        
        return {
            "type": "visualization",
            "data": f"data:image/png;base64,{img_str}"
        }
    except Exception as e:
        logger.error(f"Error generating visualization: {e}")
        raise

async def generate_forecast(df: pd.DataFrame) -> dict:
    try:
        if 'sale_date' not in df.columns or 'total_amount' not in df.columns:
            raise ValueError("DataFrame must contain 'sale_date' and 'total_amount' columns")
        
        # Prepare data for Prophet
        prophet_df = df[['sale_date', 'total_amount']].rename(columns={
            'sale_date': 'ds',
            'total_amount': 'y'
        })
        
        # Create and fit model
        model = Prophet()
        model.fit(prophet_df)
        
        # Make future predictions
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        
        # Create visualization
        fig = model.plot(forecast)
        plt.title('Sales Forecast')
        plt.xlabel('Date')
        plt.ylabel('Sales Amount')
        
        # Save plot to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        plt.close()
        
        return {
            "type": "forecast",
            "data": f"data:image/png;base64,{img_str}"
        }
    except Exception as e:
        logger.error(f"Error generating forecast: {e}")
        raise 