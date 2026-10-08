**AI Declaration:** AI used: Yes — to generate the Pandas aggregations and Streamlit boilerplate — and we can explain every part.

**Cleaning Steps:** 
Removed exact duplicates, forced `shipping_days` to be >= 0 (invalid negative days set to null), restricted `discount_pct` to bounds 0 to 1, converted `order_date` to datetime, and dropped null values to ensure accurate aggregations.

**Q1. Money:** 
Electronics is the strongest overall, bringing in the most revenue ($14.07M) and profit ($4.73M). The West region dominates geographically ($14.13M revenue, $4.57M profit). The "Sports" category is big on revenue (2nd highest at $9.4M) but noticeably weak on profit ($2.65M), falling behind Books which generated less revenue but higher profit.

**Q2. Trend:** 
Revenue remains fairly stable month-over-month (between $3.7M and $4.1M). March ($4.12M) and July ($4.13M) stand out as peak revenue and profit months, likely driven by seasonal shifts or mid-year sales events.

**Q3. Problems:** 
Returns happen most frequently in the Books (380) and Electronics (377) categories. The correlation matrix shows values of 0.007, -0.014, and 0.003, proving there is absolutely zero linear relationship between shipping days, discounts, and customer rating.

**Q4. Customers:** 
The most valuable cities are clustered heavily in the West/Northwest: Mumbai, Pune, Ahmedabad, Surat, and Jaipur. 

**Q5. Action Plan:**
1. **Audit Sports Margins:** Sports generates $9.4M in revenue but only $2.65M in profit. We must investigate supplier costs or reduce discount percentages on Sports products to align its profit margin with the Books category.
2. **Geographic Doubling Down:** The West region generates nearly double the revenue ($14.1M) of the Central ($7.2M) and East ($6.1M) regions. Reallocate 20% of the marketing budget from the East to capitalize on high-value clusters in Mumbai and Pune.
3. **Investigate Books Quality Control:** Books have the highest number of raw returns (380) despite not being the highest revenue category. We need to audit the packaging process to see if books are arriving damaged.