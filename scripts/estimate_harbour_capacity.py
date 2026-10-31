"""Reproducible, exploratory area model. Published counts always take precedence."""
from collections import Counter
import math
from statistics import median

MODEL_ID = 'area-log-municipality-balanced-v1'


def fit(rows, method='balanced_log'):
    if method == 'median_density':
        return (median(r['count'] / r['area'] for r in rows), 1)
    frequencies = Counter(r['municipality'] for r in rows)
    weighted = [(math.log(r['area']), math.log(r['count']), 1 / frequencies[r['municipality']]) for r in rows]
    total = sum(w for _, _, w in weighted)
    mx = sum(x * w for x, _, w in weighted) / total
    my = sum(y * w for _, y, w in weighted) / total
    variance = sum(w * (x - mx) ** 2 for x, _, w in weighted)
    if variance <= 0:
        raise ValueError('Training areas must vary')
    slope = sum(w * (x - mx) * (y - my) for x, y, w in weighted) / variance
    return (math.exp(my - slope * mx), slope)


def predict(parameters, area):
    coefficient, exponent = parameters
    return coefficient * area ** exponent


def cross_validate(rows, method):
    """Hold out the entire municipality, including both halves of shared facilities."""
    folds = {}
    predictions = []
    for row in rows:
        key = tuple(row['municipalities'])
        if key not in folds:
            train = [r for r in rows if not set(r['municipalities']).intersection(key)]
            folds[key] = fit(train, method)
        predicted = predict(folds[key], row['area'])
        predictions.append(dict(gid=row['gid'], observed=row['count'], predicted=predicted,
                                absolute_percentage_error=abs(predicted - row['count']) / row['count'],
                                log_residual=math.log(row['count'] / predicted),
                                held_out_municipalities=list(key)))
    return predictions


def residual_factor(rows, predictions):
    # Every municipality has equal weight, so 62 Sandefjord records cannot dominate calibration.
    frequencies = Counter(r['municipality'] for r in rows)
    weighted = sorted((abs(p['log_residual']), 1 / frequencies[r['municipality']])
                      for r, p in zip(rows, predictions))
    target = .9 * sum(w for _, w in weighted)
    cumulative = 0
    for residual, weight in weighted:
        cumulative += weight
        if cumulative >= target:
            return math.exp(residual)
    return math.exp(weighted[-1][0])


def summary(predictions):
    return dict(median_absolute_percentage_error=median(p['absolute_percentage_error'] for p in predictions),
                within_factor_two=sum(abs(p['log_residual']) <= math.log(2) for p in predictions) / len(predictions),
                mean_absolute_error=sum(abs(p['predicted'] - p['observed']) for p in predictions) / len(predictions))


def estimate(features):
    groups = {}
    for f in features:
        p = f['properties']
        r = groups.setdefault(p['gid'], dict(gid=p['gid'], name=p['name'], area=0, municipalities=set(),
                                             capacity=p.get('capacity'), possible=False))
        r['area'] += p['area']
        r['municipalities'].add(p['mun'])
        r['possible'] |= p['cls'] == 'mulig_smabathavn'
    rows = []
    for gid, r in sorted(groups.items()):
        r['municipalities'] = sorted(r['municipalities'])
        r['municipality'] = r['municipalities'][0]
        if r['capacity'] and r['capacity']['count'] > 0 and r['area'] > 0:
            rows.append(dict(gid=gid, name=r['name'], area=r['area'], count=r['capacity']['count'],
                             municipalities=r['municipalities'], municipality=r['municipality'],
                             source=r['capacity']['source'], reference_period=r['capacity']['period']))
    validation = cross_validate(rows, 'balanced_log')
    baseline = cross_validate(rows, 'median_density')
    parameters = fit(rows)
    factor = residual_factor(rows, validation)
    minimum, maximum = min(r['area'] for r in rows), max(r['area'] for r in rows)
    estimates = {}
    for gid, r in groups.items():
        if r['capacity'] or r['area'] <= 0:
            continue
        point = predict(parameters, r['area'])
        # Round outwards, to avoid pretending to know individual berths.
        low = max(0, math.floor(point / factor / 10) * 10)
        high = math.ceil(point * factor / 10) * 10
        outside = not minimum <= r['area'] <= maximum
        category = ('uncertain' if outside or r['possible'] else
                    'likely_ge_200' if low >= 200 else 'likely_lt_200' if high < 200 else 'uncertain')
        estimates[gid] = dict(model=MODEL_ID, area_m2=r['area'], count=max(10, round(point / 10) * 10), low=low, high=high,
                              category=category, outside_training_range=outside, possible_harbour=r['possible'])
    report = dict(model=MODEL_ID, purpose='Exploratory prioritisation of capacity source research; not a berth inventory or regulatory assessment.',
                  equation='count = coefficient * total_group_area_m2 ** exponent',
                  coefficient=parameters[0], exponent=parameters[1],
                  training_groups=len(rows), training_municipalities=len({m for r in rows for m in r['municipalities']}),
                  training_distribution=dict(sorted(Counter(r['municipality'] for r in rows).items())),
                  area_range_m2=[minimum, maximum],
                  validation='Leave municipalities out; shared groups are excluded from training whenever either municipality is held out.',
                  evaluation=summary(validation), baseline_median_density_evaluation=summary(baseline),
                  uncertainty=dict(multiplicative_factor=factor, calibration='90th percentile of absolute municipality-balanced held-out log errors; descriptive, not a guaranteed 90% interval.',
                                   caveats=['Sparse, nonrandom sample; published counts may be old, approximate or differ in scope. Municipality weights use the first sorted municipality for shared groups.',
                                            'Interval calibration reuses validation residuals and has no independent coverage test.',
                                            'Geometry, boat sizes and layouts vary. Possible harbours and extrapolations stay uncertain.',
                                            'No land-storage capacity is added. Published counts are never replaced.']),
                  estimated_groups=len(estimates), categories=dict(Counter(e['category'] for e in estimates.values())),
                  training=rows, held_out_predictions=validation)
    return estimates, report
