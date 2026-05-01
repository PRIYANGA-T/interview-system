"""
Aptitude MCQ Question Bank
Each topic contains 10 intermediate-to-advanced MCQs with hints.
"""

APTITUDE_TOPICS = [
    {
        'id': 'percentage',
        'title': 'Percentage',
        'description': 'Increase/decrease, successive changes, and percentage-based reasoning.'
    },
    {
        'id': 'ratio-proportion',
        'title': 'Ratio and Proportion',
        'description': 'Equivalent ratios, proportional division, and direct proportion.'
    },
    {
        'id': 'time-work',
        'title': 'Time and Work',
        'description': 'Work rates, efficiency, and combined work problems.'
    },
    {
        'id': 'average',
        'title': 'Average',
        'description': 'Weighted averages, replacement, and grouped averages.'
    },
    {
        'id': 'problem-on-age',
        'title': 'Problem on Age',
        'description': 'Basic age equations with past/future age relationships.'
    },
    {
        'id': 'problem-on-ages',
        'title': 'Problem on Ages',
        'description': 'Advanced age puzzles with ratios, products, and replacements.'
    },
    {
        'id': 'calendar-clock',
        'title': 'Calendar and Clock',
        'description': 'Clock angles, odd days, leap years, and day progression.'
    },
    {
        'id': 'pipes-cistern',
        'title': 'Pipes and Cistern',
        'description': 'Fill-empty rates, leaks, and combined flow calculations.'
    },
    {
        'id': 'profit-loss',
        'title': 'Profit and Loss',
        'description': 'Discounts, markups, cost/selling price, and net gain/loss.'
    },
    {
        'id': 'probability',
        'title': 'Probability',
        'description': 'Classical probability across cards, dice, and combinational events.'
    }
]

APTITUDE_QUESTION_BANK = {
    'percentage': [
        {'id': 1, 'question': 'A salary of ₹480 is increased by 25%. What is the new salary?', 'options': ['₹560', '₹600', '₹620', '₹640'], 'correct_option': 1, 'hint': 'Find 25% of 480 and add it.'},
        {'id': 2, 'question': 'A number is decreased by 20% and becomes 64. What was the original number?', 'options': ['72', '76', '80', '84'], 'correct_option': 2, 'hint': '64 represents 80% of original.'},
        {'id': 3, 'question': 'In a class, 72 students pass and 56 fail. What is the pass percentage?', 'options': ['54.25%', '55%', '56.25%', '57.5%'], 'correct_option': 2, 'hint': 'Pass % = pass/total × 100.'},
        {'id': 4, 'question': 'A value is increased by 10% and then decreased by 10%. Net change is:', 'options': ['0%', '1% decrease', '1% increase', '2% decrease'], 'correct_option': 1, 'hint': 'Successive % change formula: a + b + (ab/100).'},
        {'id': 5, 'question': '45 is what percent of 60?', 'options': ['70%', '72%', '75%', '80%'], 'correct_option': 2, 'hint': 'Use part/base × 100.'},
        {'id': 6, 'question': '15% of a number is 63. Find the number.', 'options': ['380', '400', '420', '440'], 'correct_option': 2, 'hint': 'Number = 63 ÷ 0.15.'},
        {'id': 7, 'question': 'A is 40% more than B, and B is 25% more than C. If A = 140, then C = ?', 'options': ['75', '80', '85', '90'], 'correct_option': 1, 'hint': 'Work backward: A → B → C.'},
        {'id': 8, 'question': 'Population increases by 20% in year 1 and 25% in year 2. Total increase is:', 'options': ['45%', '47%', '50%', '52%'], 'correct_option': 2, 'hint': 'Multiply growth factors: 1.2 × 1.25.'},
        {'id': 9, 'question': 'An item marked ₹800 is sold for ₹680. Discount percentage is:', 'options': ['12%', '13.5%', '15%', '17%'], 'correct_option': 2, 'hint': 'Discount = (MP−SP)/MP × 100.'},
        {'id': 10, 'question': 'A test score rises from 35 to 42. Percentage increase is:', 'options': ['18%', '20%', '22%', '24%'], 'correct_option': 1, 'hint': 'Increase/base × 100 = 7/35 × 100.'}
    ],
    'ratio-proportion': [
        {'id': 1, 'question': 'If ratio is 3:5 and sum is 64, the larger number is:', 'options': ['32', '36', '40', '44'], 'correct_option': 2, 'hint': 'Let numbers be 3x and 5x.'},
        {'id': 2, 'question': 'If a:b = 4:7 and b:c = 14:15, and a = 24, find c.', 'options': ['42', '45', '48', '52'], 'correct_option': 1, 'hint': 'Make b common first, then scale.'},
        {'id': 3, 'question': 'Divide 360 in ratio 2:3:4. Largest part is:', 'options': ['120', '140', '150', '160'], 'correct_option': 3, 'hint': 'Total parts = 9.'},
        {'id': 4, 'question': 'If x:y = 5:8 and y:z = 4:7, then x:z = ?', 'options': ['5:14', '5:7', '10:21', '8:14'], 'correct_option': 0, 'hint': 'Equalize y values.'},
        {'id': 5, 'question': 'Fourth proportional to 6, 9, 15 is:', 'options': ['20', '21', '22.5', '24'], 'correct_option': 2, 'hint': '6:9 = 15:x.'},
        {'id': 6, 'question': 'Mean proportional between 16 and 25 is:', 'options': ['18', '19', '20', '21'], 'correct_option': 2, 'hint': 'Use geometric mean √(16×25).'},
        {'id': 7, 'question': 'If a:b = 2:3 and b:c = 5:7, then a:c = ?', 'options': ['2:7', '10:21', '5:21', '6:35'], 'correct_option': 1, 'hint': 'Set b equal using LCM of 3 and 5.'},
        {'id': 8, 'question': 'Boys:girls = 7:5 in a class of 360. Number of girls is:', 'options': ['140', '145', '150', '155'], 'correct_option': 2, 'hint': 'Girls part = 5/12 of total.'},
        {'id': 9, 'question': 'Two numbers are in ratio 9:11 and differ by 26. Sum is:', 'options': ['234', '248', '260', '286'], 'correct_option': 2, 'hint': 'Difference corresponds to 2 parts.'},
        {'id': 10, 'question': 'If x/18 = 5/6, then x = ?', 'options': ['12', '14', '15', '16'], 'correct_option': 2, 'hint': 'Cross multiply.'}
    ],
    'time-work': [
        {'id': 1, 'question': 'A can do a job in 12 days and B in 18 days. Together they finish in:', 'options': ['7.2 days', '7.5 days', '8 days', '8.4 days'], 'correct_option': 0, 'hint': 'Add daily work rates.'},
        {'id': 2, 'question': 'A is twice as efficient as B. Together they complete work in 8 days. B alone takes:', 'options': ['16 days', '20 days', '24 days', '28 days'], 'correct_option': 2, 'hint': 'Let B rate = r, A = 2r.'},
        {'id': 3, 'question': 'A can finish in 15 days, B in 10 days. A works 5 days, then B finishes remaining work. Total days:', 'options': ['20', '22', '25', '27'], 'correct_option': 2, 'hint': 'Find work done by A in first 5 days.'},
        {'id': 4, 'question': '12 men complete work in 18 days. In how many days will 16 men finish it?', 'options': ['12', '13.5', '14', '15'], 'correct_option': 1, 'hint': 'Use man-days constant.'},
        {'id': 5, 'question': 'A, B, C can complete in 20, 30, 60 days respectively. Time to do 60% work together:', 'options': ['5', '6', '7', '8'], 'correct_option': 1, 'hint': 'Combined rate first, then multiply by fraction of work.'},
        {'id': 6, 'question': 'A and B together complete in 12 days. B alone takes 20 days. A alone takes:', 'options': ['24', '28', '30', '32'], 'correct_option': 2, 'hint': 'A rate = (A+B) rate − B rate.'},
        {'id': 7, 'question': 'Efficiency ratio A:B = 3:2. If A takes 10 days, B takes:', 'options': ['12', '14', '15', '18'], 'correct_option': 2, 'hint': 'Time is inversely proportional to efficiency.'},
        {'id': 8, 'question': '8 workers at 6 hrs/day finish in 15 days. 12 workers at 8 hrs/day need:', 'options': ['6.5 days', '7 days', '7.5 days', '8 days'], 'correct_option': 2, 'hint': 'Work ∝ workers × hours × days.'},
        {'id': 9, 'question': 'A finishes 40% of a task in 8 days. A alone completes full task in:', 'options': ['18', '20', '22', '24'], 'correct_option': 1, 'hint': 'Use direct proportion from 40% to 100%.'},
        {'id': 10, 'question': 'A and B complete work in 6 days. A alone takes 10 days. B alone takes:', 'options': ['12', '15', '18', '20'], 'correct_option': 1, 'hint': 'B rate = (A+B) − A.'}
    ],
    'average': [
        {'id': 1, 'question': 'Average of 8 numbers is 42. If one more number is added, average becomes 44. Added number is:', 'options': ['56', '58', '60', '62'], 'correct_option': 2, 'hint': 'Compare old and new totals.'},
        {'id': 2, 'question': 'Average of first five even natural numbers is:', 'options': ['5', '6', '7', '8'], 'correct_option': 1, 'hint': 'Numbers are 2, 4, 6, 8, 10.'},
        {'id': 3, 'question': 'Average of 40 students is 36. Including teacher, average becomes 37. Teacher age is:', 'options': ['72', '74', '77', '80'], 'correct_option': 2, 'hint': 'Find total increase in sum.'},
        {'id': 4, 'question': 'Average of A, B, C is 28. Average of A and B is 24. Then C is:', 'options': ['32', '34', '36', '38'], 'correct_option': 2, 'hint': 'Use total sums.'},
        {'id': 5, 'question': 'Average of 12 numbers is 15. If one number 27 is removed, new average is:', 'options': ['13.5', '13.91', '14.25', '14.5'], 'correct_option': 1, 'hint': 'Subtract removed value from total, divide by 11.'},
        {'id': 6, 'question': 'A car travels 60 km at 30 km/h and next 60 km at 20 km/h. Average speed is:', 'options': ['22', '24', '25', '26'], 'correct_option': 1, 'hint': 'Average speed = total distance / total time.'},
        {'id': 7, 'question': 'Average of three consecutive integers is 27. Largest integer is:', 'options': ['27', '28', '29', '30'], 'correct_option': 1, 'hint': 'Middle number equals average.'},
        {'id': 8, 'question': 'Average of 10 items is 15. One item added makes average 16. Added item is:', 'options': ['24', '25', '26', '27'], 'correct_option': 2, 'hint': 'New sum − old sum.'},
        {'id': 9, 'question': 'Sum of 5 numbers is 125. Their average is:', 'options': ['20', '22', '24', '25'], 'correct_option': 3, 'hint': 'Average = sum/count.'},
        {'id': 10, 'question': 'Average marks of boys is 70, girls is 80. If boys:girls = 3:2, class average is:', 'options': ['72', '73', '74', '75'], 'correct_option': 2, 'hint': 'Use weighted average.'}
    ],
    'problem-on-age': [
        {'id': 1, 'question': 'Father is 3 times son. Sum of their ages is 72. Son age is:', 'options': ['16', '18', '20', '22'], 'correct_option': 1, 'hint': 'Let son = x, father = 3x.'},
        {'id': 2, 'question': '4 years ago ratio of A:B was 5:3, now it is 7:5. Present age of A is:', 'options': ['12', '14', '16', '18'], 'correct_option': 1, 'hint': 'Form two linear equations from both ratios.'},
        {'id': 3, 'question': 'Mother is 2.5 times daughter. After 8 years, ratio becomes 2:1. Daughter age now:', 'options': ['14', '16', '18', '20'], 'correct_option': 1, 'hint': 'Use present ages as variables and set future ratio.'},
        {'id': 4, 'question': 'A is 6 years older than B. After 5 years ratio A:B = 7:6. B now is:', 'options': ['29', '30', '31', '32'], 'correct_option': 2, 'hint': 'Express A in terms of B and apply future ratio.'},
        {'id': 5, 'question': 'Three siblings are in ratio 2:3:4 and sum of ages is 45. Oldest is:', 'options': ['18', '20', '22', '24'], 'correct_option': 1, 'hint': 'Total parts = 9.'},
        {'id': 6, 'question': '5 years ago father was 7 times son. After 5 years father will be 3 times son. Son now is:', 'options': ['8', '10', '12', '14'], 'correct_option': 1, 'hint': 'Create two equations with present ages.'},
        {'id': 7, 'question': 'Present ages ratio is 4:5. After 6 years ratio becomes 5:6. Younger age now:', 'options': ['22', '24', '26', '28'], 'correct_option': 1, 'hint': 'Let ages be 4x and 5x.'},
        {'id': 8, 'question': 'A is 20% less than B. If their difference is 8, B is:', 'options': ['36', '38', '40', '42'], 'correct_option': 2, 'hint': 'A = 0.8B and B − A = 8.'},
        {'id': 9, 'question': 'Present ratio father:son = 3:1. After 6 years, ratio = 7:3. Son now is:', 'options': ['10', '12', '14', '16'], 'correct_option': 1, 'hint': 'Use ratio equations with same variable.'},
        {'id': 10, 'question': 'A is twice B now. 8 years ago A was three times B. B now is:', 'options': ['14', '15', '16', '18'], 'correct_option': 2, 'hint': 'Set A = 2B and use past condition.'}
    ],
    'problem-on-ages': [
        {'id': 1, 'question': 'Sum of ages of A and B is 50. Five years ago, their product was 144. Older age is:', 'options': ['39', '40', '41', '42'], 'correct_option': 2, 'hint': 'Use (A+B) and (A−5)(B−5).'},
        {'id': 2, 'question': 'Present ages ratio A:B:C = 4:5:6. After 5 years, sum becomes 60. Present age of C:', 'options': ['16', '18', '20', '22'], 'correct_option': 1, 'hint': 'Find present total first, then split by ratio.'},
        {'id': 3, 'question': 'A is 4 years younger than B and 6 years older than C. If sum of ages is 72, age of B:', 'options': ['26', '27', '28', '29'], 'correct_option': 2, 'hint': 'Express all ages in terms of B.'},
        {'id': 4, 'question': 'Grandfather:father:son = 12:7:2 and sum = 105. Father age is:', 'options': ['30', '35', '40', '45'], 'correct_option': 1, 'hint': 'Total parts = 21.'},
        {'id': 5, 'question': '10 years hence A will be twice B; 10 years ago A was thrice B. A now is:', 'options': ['60', '65', '70', '75'], 'correct_option': 2, 'hint': 'Solve simultaneous linear equations.'},
        {'id': 6, 'question': 'Mother is 24 years older than son. After 6 years mother is twice son. Son now is:', 'options': ['16', '18', '20', '22'], 'correct_option': 1, 'hint': 'M = S + 24 and future relation.'},
        {'id': 7, 'question': 'Present ratio of three persons is 2:3:4 and sum is 108. Oldest is:', 'options': ['40', '44', '48', '52'], 'correct_option': 2, 'hint': 'Scale ratio by total.'},
        {'id': 8, 'question': 'A is 75% of B now. After 8 years ratio becomes 5:6. B now is:', 'options': ['12', '14', '16', '18'], 'correct_option': 2, 'hint': 'Set A = 0.75B and apply future ratio.'},
        {'id': 9, 'question': 'Difference between father and son is 28. Four years ago father was 5 times son. Son now:', 'options': ['10', '11', '12', '13'], 'correct_option': 1, 'hint': 'Use difference + past relation.'},
        {'id': 10, 'question': 'Average age of 5 members is 24. One member replaced by person aged 30, average rises by 2. Replaced age:', 'options': ['18', '20', '22', '24'], 'correct_option': 1, 'hint': 'Total increase equals 5 × 2.'}
    ],
    'calendar-clock': [
        {'id': 1, 'question': 'Angle between clock hands at 3:30 is:', 'options': ['60°', '75°', '90°', '105°'], 'correct_option': 1, 'hint': 'Hour hand moves 0.5° per minute.'},
        {'id': 2, 'question': 'Mirror image time of 7:20 is:', 'options': ['4:30', '4:35', '4:40', '4:45'], 'correct_option': 2, 'hint': 'Use 11:60 − given time.'},
        {'id': 3, 'question': 'If today is Monday, day after 100 days will be:', 'options': ['Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'correct_option': 1, 'hint': 'Find remainder when divided by 7.'},
        {'id': 4, 'question': 'Which is a leap year?', 'options': ['1900', '2000', '2100', '2200'], 'correct_option': 1, 'hint': 'Century years must be divisible by 400.'},
        {'id': 5, 'question': 'Time interval between two successive overlaps of clock hands is:', 'options': ['60 min', '65 5/11 min', '66 min', '70 min'], 'correct_option': 1, 'hint': 'Standard clock overlap interval.'},
        {'id': 6, 'question': 'Angle between hands at 6:00 is:', 'options': ['150°', '170°', '180°', '190°'], 'correct_option': 2, 'hint': 'Hands opposite each other.'},
        {'id': 7, 'question': '1 Jan 2024 was Monday. 1 Jan 2025 is:', 'options': ['Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'correct_option': 1, 'hint': '2024 is a leap year, so shift by 2 days.'},
        {'id': 8, 'question': 'Angle between hands at 12:15 is:', 'options': ['75°', '80°', '82.5°', '90°'], 'correct_option': 2, 'hint': 'Minute hand at 90°, hour hand at 7.5°.'},
        {'id': 9, 'question': 'If today is Friday, day after 45 days will be:', 'options': ['Sunday', 'Monday', 'Tuesday', 'Wednesday'], 'correct_option': 1, 'hint': '45 mod 7 = 3.'},
        {'id': 10, 'question': 'Number of odd days in 400 years is:', 'options': ['0', '1', '2', '3'], 'correct_option': 0, 'hint': '400-year Gregorian cycle repeats exactly.'}
    ],
    'pipes-cistern': [
        {'id': 1, 'question': 'Pipe A fills in 6h and B in 8h. Together they fill tank in:', 'options': ['3.2h', '3.43h', '3.75h', '4h'], 'correct_option': 1, 'hint': 'Add filling rates.'},
        {'id': 2, 'question': 'A fills in 5h, leak empties in 20h. Net filling time:', 'options': ['6h', '6.67h', '7h', '7.5h'], 'correct_option': 1, 'hint': 'Net rate = fill rate − leak rate.'},
        {'id': 3, 'question': 'Three pipes fill in 10h, 12h, 15h. Together they fill in:', 'options': ['3h', '4h', '4.5h', '5h'], 'correct_option': 1, 'hint': 'Use LCM-based rate addition.'},
        {'id': 4, 'question': 'A pipe fills in 8h and a leak empties in 24h. Both open, tank fills in:', 'options': ['10h', '12h', '14h', '16h'], 'correct_option': 1, 'hint': '1/8 − 1/24 = 1/12.'},
        {'id': 5, 'question': 'Pipes fill in 6h and 9h together for 2h, then slower pipe closed. Time to finish by faster pipe:', 'options': ['2h', '2.67h', '3h', '3.5h'], 'correct_option': 1, 'hint': 'Find work done in first 2h, then remaining.'},
        {'id': 6, 'question': 'A pipe fills tank in 4h but is closed 10 min every hour. Total time needed:', 'options': ['4h 30m', '4h 48m', '5h', '5h 12m'], 'correct_option': 1, 'hint': 'Effective hourly fill = 50/60 of normal fill per hour.'},
        {'id': 7, 'question': 'Inlet fills in 12h. Outlet empties in 18h. Outlet opened after 3h. Total fill time:', 'options': ['24h', '27h', '30h', '33h'], 'correct_option': 2, 'hint': 'First fill part, then net rate for remainder.'},
        {'id': 8, 'question': 'Pipes fill in 15h and 20h; third empties in 30h. All open, tank fills in:', 'options': ['10h', '11h', '12h', '13h'], 'correct_option': 2, 'hint': 'Add two inlets and subtract outlet rate.'},
        {'id': 9, 'question': 'A fills in 10h and B empties in 15h. If each runs 1h alternately starting with A, fraction filled after 2h:', 'options': ['1/20', '1/30', '1/40', '1/50'], 'correct_option': 1, 'hint': 'Net in two hours = A one hour − B one hour.'},
        {'id': 10, 'question': 'One pipe fills half tank in 2h. With second pipe together full tank fills in 3h. Second pipe alone fills in:', 'options': ['8h', '10h', '12h', '14h'], 'correct_option': 2, 'hint': 'Convert half-in-2h to full rate first.'}
    ],
    'profit-loss': [
        {'id': 1, 'question': 'Cost price is ₹500 and selling price is ₹575. Profit % is:', 'options': ['12%', '15%', '18%', '20%'], 'correct_option': 1, 'hint': 'Profit % = profit/CP × 100.'},
        {'id': 2, 'question': 'Marked price ₹800, discount 10%, CP ₹640. Profit % is:', 'options': ['10%', '12.5%', '15%', '18%'], 'correct_option': 1, 'hint': 'Find SP after discount first.'},
        {'id': 3, 'question': 'An item sold for ₹360 at 20% loss. Cost price is:', 'options': ['420', '440', '450', '480'], 'correct_option': 2, 'hint': 'SP = 80% of CP.'},
        {'id': 4, 'question': 'If profit is 25% and profit amount is ₹50, selling price is:', 'options': ['₹225', '₹240', '₹250', '₹260'], 'correct_option': 2, 'hint': '0.25 × CP = 50.'},
        {'id': 5, 'question': 'Successive discounts 20% and 10% on ₹1000 give final price:', 'options': ['₹700', '₹710', '₹720', '₹730'], 'correct_option': 2, 'hint': 'Apply discounts one after another.'},
        {'id': 6, 'question': 'A trader uses 800g as 1kg and sells at cost price. Gain % is:', 'options': ['20%', '22.5%', '25%', '30%'], 'correct_option': 2, 'hint': 'Revenue for 1kg equals price of only 800g.'},
        {'id': 7, 'question': 'SP is ₹230 at 15% profit. CP is:', 'options': ['₹180', '₹190', '₹200', '₹210'], 'correct_option': 2, 'hint': 'SP = 1.15 × CP.'},
        {'id': 8, 'question': 'At ₹540 there is 10% loss. For 20% profit, new SP should be:', 'options': ['₹680', '₹700', '₹720', '₹740'], 'correct_option': 2, 'hint': 'First find CP using 90% relation.'},
        {'id': 9, 'question': 'Two articles sold at ₹1000 each; one at 20% gain and one at 20% loss. Net result:', 'options': ['No profit no loss', '2% loss', '4% loss', '4% gain'], 'correct_option': 2, 'hint': 'Equal SP with equal ±% leads to net loss.'},
        {'id': 10, 'question': 'Item marked 40% above CP, then discounted by 25%. Net profit % is:', 'options': ['3%', '5%', '7%', '10%'], 'correct_option': 1, 'hint': 'Take CP = 100 for quick computation.'}
    ],
    'probability': [
        {'id': 1, 'question': 'Probability of getting exactly one head in two fair tosses:', 'options': ['1/4', '1/3', '1/2', '3/4'], 'correct_option': 2, 'hint': 'List all equally likely outcomes.'},
        {'id': 2, 'question': 'Probability of getting an even number on a fair die:', 'options': ['1/3', '1/2', '2/3', '5/6'], 'correct_option': 1, 'hint': 'Favorable outcomes are 2,4,6.'},
        {'id': 3, 'question': 'Bag has 3 red and 2 blue balls. Probability of red on one draw:', 'options': ['2/5', '3/5', '4/5', '1/2'], 'correct_option': 1, 'hint': 'Favorable/total.'},
        {'id': 4, 'question': 'Probability of drawing two aces from a deck (without replacement):', 'options': ['1/169', '1/221', '1/244', '1/325'], 'correct_option': 1, 'hint': 'Multiply sequential probabilities.'},
        {'id': 5, 'question': 'Probability of drawing a king or queen from 52 cards:', 'options': ['1/13', '2/13', '3/13', '4/13'], 'correct_option': 1, 'hint': 'Kings + queens = 8 favorable cards.'},
        {'id': 6, 'question': 'Probability that sum of two dice is 7:', 'options': ['1/12', '1/8', '1/6', '1/5'], 'correct_option': 2, 'hint': 'Count favorable ordered pairs.'},
        {'id': 7, 'question': 'Probability of at least one head in 3 tosses:', 'options': ['5/8', '3/4', '7/8', '1'], 'correct_option': 2, 'hint': 'Use complement: 1 − P(no heads).'},
        {'id': 8, 'question': 'Probability that a randomly chosen year is leap year (Gregorian cycle):', 'options': ['1/4', '97/400', '99/400', '3/16'], 'correct_option': 1, 'hint': 'Use 400-year cycle counts.'},
        {'id': 9, 'question': 'From word LEVEL, probability of choosing letter E:', 'options': ['1/5', '2/5', '3/5', '1/2'], 'correct_option': 1, 'hint': 'Count repeated letters carefully.'},
        {'id': 10, 'question': 'Box has 5 white, 4 black balls. Two drawn without replacement. Probability of different colors:', 'options': ['4/9', '1/2', '5/9', '2/3'], 'correct_option': 2, 'hint': 'Use WW/BB complement or direct WB + BW.'}
    ]
}
