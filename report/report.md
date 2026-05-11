# The Invisible Tax: Quantifying the Immigrant Housing Penalty Across Four Canadian Cities

## Abstract

An immigrant household in Richmond Hill spends 33 cents of every dollar on rent. A non-immigrant household in the same city, earning similar income, spends 27 cents. This gap is not explained by poverty. It is not explained by location. After controlling for both income and city, immigrant households across Canada's four largest metropolitan areas pay 2.92 percentage points more of their income on housing than non-immigrants. In Toronto, that penalty reaches 5.37 percentage points, a statistically significant result that holds regardless of how much a household earns.

## 1. Introduction

Canada welcomes hundreds of thousands of new permanent residents every year. Most of them settle in four cities: Montreal, Toronto, Edmonton, and Vancouver. When they arrive, they rent. They sign new leases. And according to the Canada Mortgage and Housing Corporation, new tenants in Toronto paid 44% more than long-term tenants for the same unit in 2024. Immigrants are almost always new tenants. They absorb the full weight of a rental market that rewards staying and punishes arriving.

This paper uses CMHC census subdivision data from 194 neighbourhoods to ask one question: after accounting for income and location, do immigrant households pay more for housing than non-immigrants? The answer is yes, and the size of that gap varies by city in ways that carry direct consequences for housing policy.

## 2. Data and Methods

The dataset contains shelter-to-income ratio measurements for 194 census subdivisions across Montreal, Toronto, Edmonton, and Vancouver, separated by immigrant status and housing tenure. The shelter-to-income ratio, or STIR, measures the share of household income spent on shelter costs. A STIR above 30% is the CMHC threshold for housing unaffordability.

After cleaning, the dataset contains 582 rows across three immigrant status categories. City-level rows were separated from neighbourhood-level rows to allow both broad and local analysis.

Three methods were used. First, descriptive analysis compared STIR by city, tenure, and immigrant status across all four cities. Second, a linear regression model predicted STIR using household income, city, and immigrant status to isolate the independent effect of being an immigrant after holding the other factors constant. An interaction model then extended this by estimating the immigrant penalty separately for each city. Third, a K-means clustering algorithm grouped immigrant neighbourhoods into four types based on their full housing burden profile, allowing neighbourhood-specific policy recommendations to be developed.

To explain the findings, rental market data from the CMHC 2025 Rental Market Report was used to connect the observed STIR gaps to the structure of the rental market, particularly the higher rents charged to new tenants when units change hands.

## 3. Findings

### 3.1 The City-Level Picture

Immigrant renters face higher housing costs in every city, but the size of that gap differs considerably. In Toronto, immigrant renters spend an average of 26.7% of income on shelter compared to 27.3% for non-immigrants at the city level. In Edmonton, immigrants spend 23.7% versus 26.3% for non-immigrants, meaning immigrants actually pay less than non-immigrants in that city. Montreal sits at 21.1% for immigrant renters versus 21.9% for non-immigrants, the lowest burden across all four cities.

These city-wide averages hide enormous variation at the neighbourhood level. Twelve individual census subdivisions show immigrant renter STIR at or above the 30% affordability threshold, including Richmond Hill at 33.1%, Vaughan at 31.8%, and Aurora at 31.5%. Every one of these neighbourhoods is in Toronto or Vancouver. Edmonton contributes zero neighbourhoods to this list.

A pattern also appears among homeowners. Immigrant homeowners pay substantially more than non-immigrant homeowners in every city. In Toronto, immigrant owners pay 23.2% STIR compared to 17.6% for non-immigrant owners. Homeownership does not remove the housing penalty.

### 3.2 The Invisible Tax

The most important finding in this analysis is that income does not explain the immigrant housing gap. A scatter plot of household income against STIR, with separate trend lines for immigrant and non-immigrant households, shows the immigrant trend line sitting persistently higher at every income level. In West Vancouver, where immigrant households earn an average of $245,000 per year, immigrant renters still spend 35.7% of their income on housing, well above the 30% threshold and well above what their earnings alone would predict.

The regression model formalizes this. After controlling for household income and city, being an immigrant adds 2.92 percentage points to STIR. This coefficient is the Invisible Tax, the part of the housing burden that belongs entirely to immigrant status and nothing else.

The interaction model breaks this down by city. The results show that the immigrant housing penalty is not spread evenly across the country.

| City | Immigrant housing penalty | Significance |
|------|--------------------------|--------------|
| Toronto | +5.37 percentage points | p less than 0.01 |
| Vancouver | +3.57 percentage points | p less than 0.01 |
| Montreal | +0.85 percentage points | Not significant |
| Edmonton | +0.85 percentage points | Not significant |

In Montreal and Edmonton, once income is controlled for, the gap between immigrant and non-immigrant housing costs is statistically indistinguishable from zero. The penalty is a Toronto and Vancouver problem, not a national one. This points directly to city-level housing market structures as the cause rather than anything specific to immigrants themselves.

### 3.3 Neighbourhood Types and the Hidden Danger Zone

Clustering immigrant neighbourhoods by their full burden profile reveals four distinct types. The largest group, 56 neighbourhoods mostly in Montreal and Edmonton, shows manageable burden and a small renter-owner gap of just 0.5 percentage points.

The most important finding from the clustering is the identification of what we call the Renter Trap. A group of 34 neighbourhoods shows average total STIR of just 19.5%, which looks affordable by conventional measures. Within these same neighbourhoods however, immigrant renter STIR reaches 26.1% on average, with a renter-owner gap of 7.8 percentage points. Neighbourhoods like Lions Bay and Sainte-Julie belong to this group. Their overall affordability figures hide a serious renter-specific crisis that standard policy tools would never detect.

### 3.4 Why This Happens

The CMHC 2025 Rental Market Report provides the explanation. New tenants in Canada's major rental markets pay substantially more than long-term tenants for the same unit. In Toronto in 2024, this turnover premium reached 44%. In Edmonton it was 5%. Immigrants almost always enter as new tenants and absorb this premium in full.

In cities with strict rent control for existing tenants, the gap between what new and established renters pay is widest, and immigrants are consistently on the expensive side of that divide. Edmonton and Montreal, with different regulatory environments and higher vacancy rates, show smaller gaps that disappear entirely once income is controlled for.

## 4. Policy Recommendations

Three recommendations follow from these findings.

First, immigrant-specific rent supplements targeted at the neighbourhoods with the highest Immigrant Housing Stress Index scores in Toronto and Vancouver would address the penalty where it is largest and most statistically robust. Concentrating support in the first five years after arrival, when households are most likely to be paying full turnover-level rents, would make the program both efficient and directly responsive to the mechanism driving the gap.

Second, turnover rent transparency requirements in high-penalty cities would help new tenants understand what the previous occupant paid before signing a lease. This reform, already in place in several European countries, would give immigrants and other new tenants the information they need to challenge excessive rent increases at the moment they are most vulnerable to them.

Third, the 34 neighbourhoods identified as Renter Trap communities need renter-specific monitoring and dedicated support. These places are invisible to conventional affordability tools because their average STIR looks acceptable. A neighbourhood-level housing stress index of the kind developed in this analysis would allow policymakers to find and prioritize these hidden problem areas before they show up in population-level statistics years later.

## 5. Conclusion

Immigrants in Toronto pay 5.37 percentage points more for housing than non-immigrants earning the same income. That number is regression-controlled and statistically significant at the one percent level. It exists because immigrants arrive as new tenants in cities where being a new tenant is expensive. It does not exist in Edmonton or Montreal at any meaningful level, which tells us this is not something about immigrants. It is something about housing markets that falls hardest on newcomers.

The Invisible Tax can be measured. It can be mapped to specific neighbourhoods. And based on the evidence in this paper, it can be reduced through targeted, city-specific policies that go after the rental market mechanisms creating it rather than treating the problem as a uniform national issue.
## References

Canada Mortgage and Housing Corporation. (2025). Rental Market Report. CMHC Housing Observer.

Canada Mortgage and Housing Corporation. (2024). Rental Market Report: Fall 2024. CMHC.

Statistics Canada. (2021). Census of Population: Housing indicators. Statistics Canada Catalogue.

Statistics Canada. (2021). Housing experiences in Canada: Recent immigrants. Statistics Canada.

Parliamentary Budget Officer. (2024). Federal spending on housing affordability. Office of the PBO.