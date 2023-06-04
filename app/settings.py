from channels import Email, PubSub, Slack

# Topics must be defined lowercase.
SALES = 'sales'
PRICING = 'pricing'
ALL = 'any'


TOPIC_MAPPING = {
    SALES: [Slack],
    PRICING: [Email],
    ALL: [Slack, Email, PubSub]
}
