def count_cycle_stats(casesCycle):
    current_cycles_stats = dict()
    current_cycles_stats['total_not_executed'] = 0
    current_cycles_stats['total_error'] = 0
    current_cycles_stats['total_blocked'] = 0
    current_cycles_stats['total_passed'] = 0
    current_cycles_stats['total'] = 0

    for item in casesCycle:
        current_cycles_stats['total_{}'.format(item.state_code.value)] += 1
        current_cycles_stats['total'] += 1
    return current_cycles_stats
