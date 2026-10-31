/* Shared classification for map, search and tour. Published capacity takes precedence. */
(function (root) {
  'use strict';
  const labels = {likely_ge_200: 'Trolig minst 200', likely_lt_200: 'Trolig under 200', uncertain: 'Usikkert antall plasser'};
  function matches(properties, mode = 'published') {
    if (properties.capacity) return properties.capacity.count >= 200;
    const estimate = properties.capacity_estimate;
    if (!estimate || mode === 'published') return false;
    if (estimate.category === 'likely_ge_200') return true;
    return mode === 'possible' && estimate.high >= 200;
  }
  root.CapacityFilter = { matches, labels };
})(typeof window === 'undefined' ? globalThis : window);
