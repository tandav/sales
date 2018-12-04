import argparse
import sys
from pyspark.sql import SparkSession
import sys


parser = argparse.ArgumentParser()
parser.add_argument('table' , type=str                )
parser.add_argument('--shop', type=int, required=False)
parser.add_argument('--item', type=int, required=False)
args = parser.parse_args()

print(args)

if not args.table:
    print('error: table is not specified')
    sys.exit(1)

spark = SparkSession.builder.getOrCreate()
df = spark.read.parquet(args.table +'_prediction')


if args.shop and args.item:
    result = df.filter((df.shop == args.shop) & (df.item == args.item))
elif args.shop:
    result = df.filter(df.shop == args.shop)
elif args.item:
    df.filter(df.item == args.item)
else:
    result = df

report  = ''
report += '='*72
report += '\n'*5

for row in result.collect():
    report += 'shop ' + str(row.shop) + ' item ' + str(row.item) + '\n'
    report += 'sales prediction for next 4 weeks:\n'

    for week in range(4):
        report += 'week' + str(week) + ' '
        week_pred = row.prediction[week * 7 : (week + 1) * 7]
        week_pred_round = [round(p) for p in week_pred]
        
        for p in week_pred_round:
            report += str(p).rjust(3) + ' '
        report += 'week sum:' + str(sum(week_pred_round)) + '\n'
    report += '\n'
    # rounded = [round(p) for p in row.prediction]
    # rounded_str = []
    # print(row.shop, row.item, end=' ')
    # for p in row.prediction:
        # print('{r:3}'.format(r=round(p)), end=' ')
    # print()
report += '\n'*5
report += '='*72

print(report)
