# Determine whether the Metafield should be included in the attributes
def should_include_metafield(metafield, bloomreach_namespace):
  # Check Product metafields
  if bloomreach_namespace == "sp":
    if metafield["namespace"] == "custom" and metafield["key"] in ["spanx_effect", "spanx_collection", "lifecycle", "final_sale", "markdown_type", "return_rate", "seasonality", "intended_use", "length", "rise", "silhouette", "compression_level", "compression_zones", "activity_level"]:
      return True
  # Check Variant metafields
  elif bloomreach_namespace == "sv":
    return False
  return False

# Determine whether the Product should be included in the Bloomreach index
def should_include_product(product):
  # Check the Product is not Archived
  if product["status"].lower() == "archived":
    return False
  # Check the Product does not have the `no_index` tag
  if product["tags"] and "no_index" in product["tags"]:
    return False
  return True