import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

METAFIELDS_CUSTOM = [
  "category",
  "combined_markdown_type",
  "dom_final_sale",
  "markdown_type"
]
METAFIELDS_CUSTOM_FIELDS = [
  "activity_level",
  "built_in_features",
  "compression_level",
  "compression_zones",
  "intended_use",
  "length",
  "length_description",
  "lifecycle",
  "return_rate",
  "rise",
  "seasonality",
  "silhouette",
  "spanx_collection",
  "spanx_effect"
]
METAFIELDS_COMBINED_LISTING = [
  "is_child",
  "is_parent",
  "parent_product"
]

# Determine whether the Metafield should be included in the attributes
def should_include_metafield(metafield, bloomreach_namespace):
  # Check Product metafields
  if bloomreach_namespace == "sp":
    # Check the `custom_fields` namespace
    if metafield["namespace"] == "custom_fields" and metafield["key"] in METAFIELDS_CUSTOM_FIELDS:
      return True
    # Check the `custom` namespace
    if metafield["namespace"] == "custom" and metafield["key"] in METAFIELDS_CUSTOM:
      return True
    # Check the `combined_listing` namespace
    if metafield["namespace"] == "combined_listing" and metafield["key"] in METAFIELDS_COMBINED_LISTING:
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

# Use legacy identifier, instead of gid
def use_legacy_identifier(shopify_identifier):
  if shopify_identifier is None:
    return None
  if "gid" in shopify_identifier:
    return shopify_identifier.split("/")[-1]
  return shopify_identifier

# Determine if the option has necessary data
def has_option_data(option):
  return "name" in option and "value" in option

# Use the option value
def get_option_value(option):
  if has_option_data(option):
    return option["value"]
  return None

# Determine the supported option attribute name
def get_supported_option_attribute_name(option):
  if has_option_data(option):
    option_name = option["name"].lower().strip()
    logger.debug(f"Option name: {option_name}")
    if "color" in option_name:
      return "color"
    if "size" in option_name:
      return "size"
    if "inseam" == option_name:
      return "inseam"
    if "band size" == option_name:
      return "band_size"
    if "cup size" == option_name:
      return "cup_size"
    if "size type" == option_name:
      return "size_type"
    if "sizing" == option_name:
      return "sizing"
  return None

# Determine whether the option is supported
def is_supported_option(option):
  return get_supported_option_attribute_name(option) is not None
