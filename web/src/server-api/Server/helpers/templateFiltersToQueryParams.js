/**
 * Convert template filters to axios request parameters.
 */
export default function templateFiltersToQueryParams({ fields, filters = {} }) {
  const params = {};
  if (fields != null && fields.length > 0) {
    params.include = fields.join(",");
  }
  return params;
}