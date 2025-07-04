# Determine whether the Metafield should be included in the attributes
def should_include_metafield(metafield, bloomreach_namespace):
  # Check Product metafields
  if bloomreach_namespace == "sp":
    # Check the `custom_fields` namespace
    if metafield["namespace"] == "custom_fields" and metafield["key"] in ["spanx_effect", "spanx_collection", "return_rate", "seasonality", "intended_use", "length", "rise", "silhouette", "compression_level", "compression_zones", "activity_level"]:
      return True
    # Check the `app--6007307--sanity-fields` namespace
    if metafield["namespace"] == "app--6007307--sanity-fields" and metafield["key"] in ["lifecycle", "domesticFinalSale", "markdown_type"]:
      return True
    # Check the `combined_listing` namespace
    if metafield["namespace"] == "combined_listing" and metafield["key"] in ["is_parent", "is_child", "parent_product"]:
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

# Use Hydrogen Status, if present
def use_hydrogen_status(product):
  # Check if the product has `Status` tags
  if product["tags"]:
    if "Status:Active" in product["tags"]:
      return "ACTIVE"
    elif "Status:Draft" in product["tags"]:
      return "DRAFT"
  # Default to regular status
  return product["status"]
