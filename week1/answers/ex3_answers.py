"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approacanch?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """


(VM_Review_Agent) xx@xx sovereign-agent-lab % cd exercise3_rasa 
(VM_Review_Agent)  exercise3_rasa % uv run rasa shell
zsh: correct 'rasa' to '.rasa' [nyae]? n
2026-04-08 22:36:35 INFO     rasa.tracing.config  - No endpoint for tracing type available in endpoints.yml, tracing will not be configured.
2026-04-08 22:36:41 INFO     root  - Starting Rasa server on http://0.0.0.0:5005
2026-04-08 22:36:42 INFO     rasa.core.processor  - Loading model models/20260408-214950-indigo-major.tar.gz...
2026-04-08 22:36:42 INFO     rasa.shared.core.domain  - [info     ] domain.from_yaml.validating
2026-04-08 22:36:42 WARNING  rasa.shared.utils.health_check.health_check  - [warning  ] The LLM_API_HEALTH_CHECK environment variable is set to false, which will disable LLM health check. It is recommended to set this variable to true in production environments. event_key=llm_based_command_generator.load.perform_llm_health_check.disabled
2026-04-08 22:36:42 INFO     rasa.dialogue_understanding.generator.llm_based_command_generator  - [info     ] llm_based_command_generator.flow_retrieval.enabled
2026-04-08 22:36:42 WARNING  rasa.shared.utils.health_check.health_check  - [warning  ] The LLM_API_HEALTH_CHECK environment variable is set to false, which will disable embeddings API health check. It is recommended to set this variable to true in production environments. event_key=flow_retrieval.load.perform_embeddings_health_check.disabled
2026-04-08 22:36:42 INFO     faiss.loader  - Loading faiss.
2026-04-08 22:36:42 INFO     faiss.loader  - Successfully loaded faiss.
2026-04-08 22:36:42 INFO     root  - Rasa server is up and running.
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking                                                                                                                                 

Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers

/Users/xx/PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:390: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='1. start flow confirm_booking \n2...unction_call=None, provider_specific_fields=None)` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...ider_specific_fields={})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_python(
I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                   

Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers

/Users/xx/PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:390: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='1. set slot guest_count 160\n2. s...unction_call=None, provider_specific_fields=None)` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...ider_specific_fields={})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_python(
And how many of those guests will need vegan meals?
Your input ->  50 vegan                                                                                                                                                     

Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers

/Users/xx/PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:390: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='1. set slot vegan_count 50\n2. pr...unction_call=None, provider_specific_fields=None)` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...ider_specific_fields={})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_python(
I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  deposit is 200                                                                                                                                               

Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers

/Users/xx/PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:390: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='To address the user\'s last messa...unction_call=None, provider_specific_fields=None)` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...ider_specific_fields={})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_python(
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
What else can I help you with?
Your input ->                                                                                                                                                               


"""

CONVERSATION_1_OUTCOME = "confimred"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
(VM_Review_Agent) xx@xx sovereign-agent-lab % cd exercise3_rasa 
(VM_Review_Agent)  exercise3_rasa % uv run rasa shell
zsh: correct 'rasa' to '.rasa' [nyae]? n
2026-04-08 22:36:35 INFO     rasa.tracing.config  - No endpoint for tracing type available in endpoints.yml, tracing will not be configured.
2026-04-08 22:36:41 INFO     root  - Starting Rasa server on http://0.0.0.0:5005
2026-04-08 22:36:42 INFO     rasa.core.processor  - Loading model models/20260408-214950-indigo-major.tar.gz...
2026-04-08 22:36:42 INFO     rasa.shared.core.domain  - [info     ] domain.from_yaml.validating
2026-04-08 22:36:42 WARNING  rasa.shared.utils.health_check.health_check  - [warning  ] The LLM_API_HEALTH_CHECK environment variable is set to false, which will disable LLM health check. It is recommended to set this variable to true in production environments. event_key=llm_based_command_generator.load.perform_llm_health_check.disabled
2026-04-08 22:36:42 INFO     rasa.dialogue_understanding.generator.llm_based_command_generator  - [info     ] llm_based_command_generator.flow_retrieval.enabled
2026-04-08 22:36:42 WARNING  rasa.shared.utils.health_check.health_check  - [warning  ] The LLM_API_HEALTH_CHECK environment variable is set to false, which will disable embeddings API health check. It is recommended to set this variable to true in production environments. event_key=flow_retrieval.load.perform_embeddings_health_check.disabled
2026-04-08 22:36:42 INFO     faiss.loader  - Loading faiss.
2026-04-08 22:36:42 INFO     faiss.loader  - Successfully loaded faiss.
2026-04-08 22:36:42 INFO     root  - Rasa server is up and running.
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking                                                                                                                                 

Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers

/Users/xx/PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:390: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='1. start flow confirm_booking \n2...unction_call=None, provider_specific_fields=None)` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...ider_specific_fields={})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_python(
I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                   

Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers

/Users/xx/PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:390: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='1. set slot guest_count 160\n2. s...unction_call=None, provider_specific_fields=None)` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...ider_specific_fields={})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_python(
And how many of those guests will need vegan meals?
Your input ->  50 vegan                                                                                                                                                     

Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers

/Users/xx/PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:390: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='1. set slot vegan_count 50\n2. pr...unction_call=None, provider_specific_fields=None)` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...ider_specific_fields={})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_python(
I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  deposit is 200                                                                                                                                               

Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers

/Users/xx/PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:390: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='To address the user\'s last messa...unction_call=None, provider_specific_fields=None)` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...ider_specific_fields={})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_python(
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
What else can I help you with?

Your input ->                                                                                                                                                               


"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "500 deposite exceeds the limit"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
026-04-09 12:15:58 DEBUG    rasa.dialogue_understanding.generator.flow_retrieval  - [debug    ] Fetched the top 20similar flows from the vector store event_key=flow_retrieval.query_vector_store.fetched query=calling to confirm a booking results=[{'flow_id': 'confirm_booking', 'score': 0.84291214, 'content': "confirm booking: Handle an inbound call from a pub manager confirming a venue booking for tonight's event. Triggered when the pub manager calls to confirm booking details, including guest count, dietary requirements, and deposit terms. This is the primary task — all booking-related calls should use this flow.\n\n    guest_count: total number of guests attending tonight's event\n    vegan_count: number of guests requiring vegan meals\n    deposit_amount_gbp: deposit amount in GBP the manager is proposing to secure the booking"}, {'flow_id': 'handle_out_of_scope', 'score': 0.7989936, 'content': 'handle out of scope: Handle requests that are outside the scope of booking confirmation, such as questions about parking, AV equipment, seating arrangements, menus, weather, or any non-booking topic.'}] top_k=20
2026-04-09 12:15:58 DEBUG    rasa.dialogue_understanding.generator.llm_based_command_generator  - [debug    ] llm_based_command_generator.predict_commands.filtered_flows enabled_flow_retrieval=True message={'text': 'calling to confirm a booking', 'message_id': 'ed0db71af4f04647879193c5f36dc43d', 'metadata': None, 'flows_from_semantic_search': [('confirm_booking', 0.8429121375083923), ('handle_out_of_scope', 0.7989935874938965)], 'flows_in_prompt': ['confirm_booking', 'handle_out_of_scope']} relevant_flows=['confirm_booking', 'handle_out_of_scope']
2026-04-09 12:15:58 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.prompt_rendered prompt=## Task Description
Your task is to analyze the current conversation context and generate a list of actions to start new business processes that we call flows, to extract slots, or respond to small talk and knowledge requests.

---

## Available Flows and Slots
Use the following structured data:
```json
{"flows":[{"name":"confirm_booking","description":"Handle an inbound call from a pub manager confirming a venue booking for tonight's event. Triggered when the pub manager calls to confirm booking details, including guest count, dietary requirements, and deposit terms. This is the primary task — all booking-related calls should use this flow.\n","slots":[{"name":"guest_count","description":"total number of guests attending tonight's event"},{"name":"vegan_count","description":"number of guests requiring vegan meals"},{"name":"deposit_amount_gbp","description":"deposit amount in GBP the manager is proposing to secure the booking"}]},{"name":"handle_out_of_scope","description":"Handle requests that are outside the scope of booking confirmation, such as questions about parking, AV equipment, seating arrangements, menus, weather, or any non-booking topic.\n"}]}
```

---

## Available Actions:
* `start flow flow_name`: Starting a flow. For example, `start flow transfer_money` or `start flow list_contacts`.
* `set slot slot_name slot_value`: Slot setting. For example, `set slot transfer_money_recipient Freddy`. Can be used to correct and change previously set values.
* `cancel flow`: Cancelling the current flow.
* `disambiguate flows flow_name1 flow_name2 ... flow_name_n`: Disambiguate which flow should be started when user input is ambiguous by listing the potential flows as options. For example, `disambiguate flows list_contacts add_contact remove_contact ...` if the user just wrote "contacts".
* `provide info`: Responding to the user's questions by supplying relevant information, such as answering FAQs or explaining services.
* `offtopic reply`: Responding to casual or social user messages that are unrelated to any flows, engaging in friendly conversation and addressing off-topic remarks.
* `hand over`: Handing over to a human, in case the user seems frustrated or explicitly asks to speak to one.
* `repeat message`: Repeating the last bot message.

---

## General Tips
* Do not fill slots with abstract values or placeholders.
* For categorical slots try to match the user message with allowed slot values. Use "other" if you cannot match it.
* Set the boolean slots based on the user response. Map positive responses to `True`, and negative to `False`.
* Extract text slot values exactly as provided by the user. Avoid assumptions, format changes, or partial extractions.
* Only use information provided by the user.
* Use clarification in ambiguous cases.
* Multiple flows can be started. If a user wants to digress into a second flow, you do not need to cancel the current flow.
* Do not cancel the flow unless the user explicitly requests it.
* Strictly adhere to the provided action format.
* Focus on the last message and take it one step at a time.
* Use the previous conversation steps only to aid understanding.

---

## Current State

You are currently not inside any flow.

---

## Conversation History

USER: calling to confirm a booking

---

## Task
Create an action list with one action per line in response to the user's last message: """"""calling to confirm a booking""""""

Your action list:
2026-04-09 12:15:58 DEBUG    rasa.shared.providers.llm._base_litellm_client  - [debug    ] base_litellm_client.formatted_response formatted_response={'id': 'chatcmpl-17bfef430ded45c39968fe24342b82a9', 'choices': ['1. start flow confirm_booking \n2. provide info'], 'created': 1775681873, 'model': 'hosted_vllm/meta-llama/Llama-3.3-70B-Instruct', 'usage': {'prompt_tokens': 745, 'completion_tokens': 12, 'total_tokens': 757}, 'additional_info': None, 'latency': None}
2026-04-09 12:15:58 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.actions_generated action_list=1. start flow confirm_booking 
2. provide info
2026-04-09 12:15:58 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.finished commands=[StartFlowCommand(flow='confirm_booking'), KnowledgeAnswerCommand()]
/Users//PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:390: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='1. start flow confirm_booking \n2...unction_call=None, provider_specific_fields=None)` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...ider_specific_fields={})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_python(
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RegexMessageHandler fn=process node_name=run_RegexMessageHandler
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - [debug    ] processor.message.parse        parse_data_entities=[] parse_data_intent={'name': None, 'confidence': 0.0} parse_data_text=calling to confirm a booking
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - Logged UserUtterance - tracker now has 4 events.
2026-04-09 12:15:58 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {}, targets: ['flows_provider'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - [debug    ] processor.extract.slots        action_extract_slot=action_extract_slots len_extraction_events=0 rasa_events=[]
2026-04-09 12:15:58 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e)}, targets: ['command_processor'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=CommandProcessorComponent fn=execute_commands node_name=command_processor
2026-04-09 12:15:58 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] command_processor.clean_up_commands.prepend_command_freeform_answer command=KnowledgeAnswerCommand()
2026-04-09 12:15:58 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] command_processor.clean_up_commands.final_commands command=[KnowledgeAnswerCommand(), StartFlowCommand(flow='confirm_booking')]
2026-04-09 12:15:58 DEBUG    rasa.dialogue_understanding.commands.start_flow_command  - [debug    ] start_flow_command.start_flow  command=StartFlowCommand(flow='confirm_booking')
2026-04-09 12:15:58 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_search previous_step_id=START
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=pattern_search next_id=pattern_search_0_utter_no_knowledge_base
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'UWQ3W6Z0', 'flow_id': 'pattern_search', 'step_id': 'pattern_search_0_utter_no_knowledge_base', 'type': 'pattern_search'}} flow_id=pattern_search step_id=pattern_search_0_utter_no_knowledge_base
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:15:58 DEBUG    rasa.core.policies.ensemble  - Made prediction using user intent.
2026-04-09 12:15:58 DEBUG    rasa.core.policies.ensemble  - Added `DefinePrevUserUtteredFeaturization(False)` event.
2026-04-09 12:15:58 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - Predicted next action 'utter_no_knowledge_base' with confidence 1.00.
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_no_knowledge_base policy_name=FlowPolicy prediction_events=[DialogueStackUpdate(""""op": "replace", "path": "/1/step_id", "value": "pattern_search_0_utter_no_knowledge_base"}]"""), FlowStarted(flow: pattern_search), <rasa.shared.core.events.DefinePrevUserUtteredFeaturization object at 0x292ae3280>]
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_no_knowledge_base rasa_events=[BotUttered('I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"metadata": {"rephrase": true}, "active_flow": "pattern_search", "step_id": "pattern_search_0_utter_no_knowledge_base", "utter_action": "utter_no_knowledge_base", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733358.951508)]
2026-04-09 12:15:58 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_search previous_step_id=pattern_search_0_utter_no_knowledge_base
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_search_0_utter_no_knowledge_base flow_id=pattern_search next_id=END
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=pattern_search step_id=END
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=confirm_booking previous_step_id=START
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=confirm_booking next_id=confirm_booking_0_collect_guest_count
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.collect          flow_id=confirm_booking step_id=confirm_booking_0_collect_guest_count
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.reset_silence_timeout_to_global collect=guest_count duration=7.0 flow_id=confirm_booking step_id=confirm_booking_0_collect_guest_count
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=START
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=pattern_collect_information next_id=start
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_0_collect_guest_count', 'collect': 'guest_count', 'utter': 'utter_ask_guest_count', 'collect_action': 'action_ask_guest_count', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=start
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:15:58 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - Predicted next action 'action_run_slot_rejections' with confidence 1.00.
2026-04-09 12:15:58 DEBUG    rasa.core.actions.action_run_slot_rejections  - [debug    ] first.collect.slot.not.set     slot_name=guest_count slot_value=None
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_run_slot_rejections policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/1"}]"""), FlowCompleted(flow: pattern_search, step_id: pattern_search_0_utter_no_knowledge_base), DialogueStackUpdate("""[{"op": "replace", "path": "/0/step_id", "value": "confirm_booking_0_collect_guest_count"}]"""), DialogueStackUpdate("""[{"op": "add", "path": "/1", "value": {"frame_id": "9WT4T1PY", "flow_id": "pattern_collect_information", "step_id": "START", "collect": "guest_count", "utter": "utter_ask_guest_count", "collect_action": "action_ask_guest_count", "rejections": [], "type": "pattern_collect_information"}}]"""), FlowStarted(flow: confirm_booking), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "start"}]"""), FlowStarted(flow: pattern_collect_information)]
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_run_slot_rejections rasa_events=[]
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - [debug    ] processor.slots.log            slots={'language': 'en', 'silence_timeout': 7.0, 'consecutive_silence_timeouts': 0.0, 'flow_hashes': {'confirm_booking': '0cfdd2e66537a1c1dc08453deb2ae383', 'handle_out_of_scope': '367e697b00b1da958c811004266f6c46', 'pattern_cancel_flow': '5edee5445ff87339ec899ab96de7ae9e', 'pattern_cannot_handle': '748dcc3783183f4c5512c2f23940b609', 'pattern_chitchat': 'aabaace3f5ef32b70351e18481c53356', 'pattern_clarification': '927f334af1fe5e570348690977bac4f2', 'pattern_code_change': 'f9db9f453c8b63fbec24c72413c86a69', 'pattern_collect_information': '072cd971740a761ddb8885f2cdc6ff20', 'pattern_completed': 'df3529f96e5d98df3f2ce63012daa641', 'pattern_continue_interrupted': '61bf7886bc116521c0d8f6f5b6760e67', 'pattern_correction': 'c35924757a8df574b91355c9a2070931', 'pattern_human_handoff': 'c021df067d37b8a23c464ca92372df6c', 'pattern_internal_error': 'b9059f3a7ca73e38b1d19ad0b09c9537', 'pattern_repeat_bot_messages': '35069cf740ceaff65ac467a58c3f77bf', 'pattern_restart': '9f4c81ddc0dcb8c4a74a141a047f0284', 'pattern_search': 'cf65ab2f7654f41f481a5f97cbcb9d9d', 'pattern_session_start': '757ea1cd44b685619e46d9c7b32c30b8', 'pattern_skip_question': '46505c0a24a5f90ab6f58a1fc69fa41b', 'pattern_user_silence': '41f05270eba1765c2fd9f1b17e1d754a', 'pattern_validate_slot': '57e5983e77f386ff93dfdcbad1c93308'}}
2026-04-09 12:15:58 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=start
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=start flow_id=pattern_collect_information next_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.predicate.evaluating      condition=slots.{{context.collect}} is not null flow_id=pattern_collect_information rendered_condition=slots.guest_count is not null
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.link.else_condition_satisfied current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information target=ask_collect
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information next_id=ask_collect
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_0_collect_guest_count', 'collect': 'guest_count', 'utter': 'utter_ask_guest_count', 'collect_action': 'action_ask_guest_count', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=ask_collect
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:15:58 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - Predicted next action 'utter_ask_guest_count' with confidence 1.00.
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_ask_guest_count policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_1_validate_{{context.collect}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "ask_collect"}]""")]
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_ask_guest_count rasa_events=[BotUttered('How many guests are you confirming for tonight's event?', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"active_flow": "confirm_booking", "step_id": "confirm_booking_0_collect_guest_count", "utter_action": "utter_ask_guest_count", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733358.968724)]
2026-04-09 12:15:58 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=ask_collect
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=ask_collect flow_id=pattern_collect_information next_id=pattern_collect_information_3_{{context.collect_action}}
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_3_{{context.collect_action}}
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_3_{{context.collect_action}} flow_id=pattern_collect_information next_id=pattern_collect_information_4_action_listen
2026-04-09 12:15:58 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_0_collect_guest_count', 'collect': 'guest_count', 'utter': 'utter_ask_guest_count', 'collect_action': 'action_ask_guest_count', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=pattern_collect_information_4_action_listen
I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
2026-04-09 12:15:58 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:15:58 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - Predicted next action 'action_listen' with confidence 1.00.
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_listen policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_3_{{context.collect_action}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_4_action_listen"}]""")]
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_listen rasa_events=[]
2026-04-09 12:15:58 DEBUG    rasa.core.tracker_stores.tracker_store  - [debug    ] No event broker configured. Skipping streaming events. event_key=tracker_store.stream_events.no_broker_configured
2026-04-09 12:15:58 DEBUG    rasa.core.processor  - [debug    ] processor.trigger_anonymization.skipping.pii_management_not_enabled
2026-04-09 12:15:58 DEBUG    rasa.core.lock_store  - [debug    ] Deleted lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._deleted_lock_for_conversation
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                   
2026-04-09 12:16:08 DEBUG    rasa.core.lock_store  - [debug    ] Issuing ticket for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store.issue_ticket
2026-04-09 12:16:08 DEBUG    rasa.core.lock_store  - [debug    ] Acquiring lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._acquiring_lock_for_conversation
2026-04-09 12:16:08 DEBUG    rasa.core.lock_store  - [debug    ] Acquired lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._acquired_lock_for_conversation
2026-04-09 12:16:08 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {}, targets: ['flows_provider'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__message__': [UserMessage(text: 160 guests, sender_id: a8e9d54b848e4ab4ab08d70f1779476e)], '__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e)}, targets: ['run_RegexMessageHandler'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=NLUMessageConverter fn=convert_user_message node_name=nlu_message_converter
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=CompactLLMCommandGenerator fn=process node_name=run_CompactLLMCommandGenerator0
2026-04-09 12:16:08 DEBUG    rasa.dialogue_understanding.utils  - [debug    ] Tracker doesn't have the 'route_session_to_calm' slot.Routing to CALM. event_key=utils.handle_via_nlu_in_coexistence.tracker_missing_route_session_to_calm_slot route_session_to_calm=[]
2026-04-09 12:16:08 DEBUG    rasa.shared.providers.embedding._base_litellm_embedding_client  - [debug    ] base_litellm_client.formatted_response formatted_response={'data': 'Embedding response data not shown here for brevity.', 'model': 'Qwen/Qwen3-Embedding-8B', 'usage': {'prompt_tokens': 2, 'completion_tokens': 0, 'total_tokens': 2}, 'additional_info': None}

Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers

2026-04-09 12:16:08 DEBUG    rasa.dialogue_understanding.generator.flow_retrieval  - [debug    ] Fetched the top 20similar flows from the vector store event_key=flow_retrieval.query_vector_store.fetched query=160 guests results=[{'flow_id': 'confirm_booking', 'score': 0.6500614, 'content': "confirm booking: Handle an inbound call from a pub manager confirming a venue booking for tonight's event. Triggered when the pub manager calls to confirm booking details, including guest count, dietary requirements, and deposit terms. This is the primary task — all booking-related calls should use this flow.\n\n    guest_count: total number of guests attending tonight's event\n    vegan_count: number of guests requiring vegan meals\n    deposit_amount_gbp: deposit amount in GBP the manager is proposing to secure the booking"}, {'flow_id': 'handle_out_of_scope', 'score': 0.5747611, 'content': 'handle out of scope: Handle requests that are outside the scope of booking confirmation, such as questions about parking, AV equipment, seating arrangements, menus, weather, or any non-booking topic.'}] top_k=20
2026-04-09 12:16:08 DEBUG    rasa.dialogue_understanding.generator.llm_based_command_generator  - [debug    ] llm_based_command_generator.predict_commands.filtered_flows enabled_flow_retrieval=True message={'text': '160 guests', 'message_id': '56f39b1760ac4bcc8f0e102b8463826c', 'metadata': None, 'flows_from_semantic_search': [('confirm_booking', 0.6500614285469055), ('handle_out_of_scope', 0.5747610926628113)], 'flows_in_prompt': ['confirm_booking', 'handle_out_of_scope']} relevant_flows=['confirm_booking', 'handle_out_of_scope']
2026-04-09 12:16:08 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.prompt_rendered prompt=## Task Description
Your task is to analyze the current conversation context and generate a list of actions to start new business processes that we call flows, to extract slots, or respond to small talk and knowledge requests.

---

## Available Flows and Slots
Use the following structured data:
```json
{"flows":[{"name":"confirm_booking","description":"Handle an inbound call from a pub manager confirming a venue booking for tonight's event. Triggered when the pub manager calls to confirm booking details, including guest count, dietary requirements, and deposit terms. This is the primary task — all booking-related calls should use this flow.\n","slots":[{"name":"guest_count","description":"total number of guests attending tonight's event"},{"name":"vegan_count","description":"number of guests requiring vegan meals"},{"name":"deposit_amount_gbp","description":"deposit amount in GBP the manager is proposing to secure the booking"}]},{"name":"handle_out_of_scope","description":"Handle requests that are outside the scope of booking confirmation, such as questions about parking, AV equipment, seating arrangements, menus, weather, or any non-booking topic.\n"}]}
```

---

## Available Actions:
* `start flow flow_name`: Starting a flow. For example, `start flow transfer_money` or `start flow list_contacts`.
* `set slot slot_name slot_value`: Slot setting. For example, `set slot transfer_money_recipient Freddy`. Can be used to correct and change previously set values.
* `cancel flow`: Cancelling the current flow.
* `disambiguate flows flow_name1 flow_name2 ... flow_name_n`: Disambiguate which flow should be started when user input is ambiguous by listing the potential flows as options. For example, `disambiguate flows list_contacts add_contact remove_contact ...` if the user just wrote "contacts".
* `provide info`: Responding to the user's questions by supplying relevant information, such as answering FAQs or explaining services.
* `offtopic reply`: Responding to casual or social user messages that are unrelated to any flows, engaging in friendly conversation and addressing off-topic remarks.
* `hand over`: Handing over to a human, in case the user seems frustrated or explicitly asks to speak to one.
* `repeat message`: Repeating the last bot message.

---

## General Tips
* Do not fill slots with abstract values or placeholders.
* For categorical slots try to match the user message with allowed slot values. Use "other" if you cannot match it.
* Set the boolean slots based on the user response. Map positive responses to `True`, and negative to `False`.
* Extract text slot values exactly as provided by the user. Avoid assumptions, format changes, or partial extractions.
* Only use information provided by the user.
* Use clarification in ambiguous cases.
* Multiple flows can be started. If a user wants to digress into a second flow, you do not need to cancel the current flow.
* Do not cancel the flow unless the user explicitly requests it.
* Strictly adhere to the provided action format.
* Focus on the last message and take it one step at a time.
* Use the previous conversation steps only to aid understanding.

---

## Current State
Use the following structured data:
```json
{"active_flow":"confirm_booking","current_step":{"requested_slot":"guest_count","requested_slot_description":"total number of guests attending tonight's event"},"slots":[{"name":"guest_count","value":"undefined","type":"float","description":"total number of guests attending tonight's event"},{"name":"vegan_count","value":"undefined","type":"float","description":"number of guests requiring vegan meals"},{"name":"deposit_amount_gbp","value":"undefined","type":"float","description":"deposit amount in GBP the manager is proposing to secure the booking"}]}
```

---

## Conversation History
USER: calling to confirm a booking
AI: I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
AI: How many guests are you confirming for tonight's event?
USER: 160 guests

---

## Task
Create an action list with one action per line in response to the user's last message: """"""160 guests""""""

Your action list:
/Users/mihalis/PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:390: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='1. set slot guest_count 160\n2. s...unction_call=None, provider_specific_fields=None)` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...ider_specific_fields={})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_python(
2026-04-09 12:16:08 DEBUG    rasa.shared.providers.llm._base_litellm_client  - [debug    ] base_litellm_client.formatted_response formatted_response={'id': 'chatcmpl-9e6b86a04b2f4bbea52b21e1075e655b', 'choices': ['1. set slot guest_count 160\n2. start flow confirm_booking'], 'created': 1775682927, 'model': 'hosted_vllm/meta-llama/Llama-3.3-70B-Instruct', 'usage': {'prompt_tokens': 900, 'completion_tokens': 16, 'total_tokens': 916}, 'additional_info': None, 'latency': None}
2026-04-09 12:16:08 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.actions_generated action_list=1. set slot guest_count 160
2. start flow confirm_booking
2026-04-09 12:16:08 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.finished commands=[SetSlotCommand(name='guest_count', value='160', extractor='LLM'), StartFlowCommand(flow='confirm_booking')]
2026-04-09 12:16:08 DEBUG    rasa.dialogue_understanding.generator.llm_based_command_generator  - [debug    ] command_processor.check_commands_against_slot_mappings.active_flow active_flow=confirm_booking
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RegexMessageHandler fn=process node_name=run_RegexMessageHandler
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.message.parse        parse_data_entities=[] parse_data_intent={'name': None, 'confidence': 0.0} parse_data_text=160 guests
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - Logged UserUtterance - tracker now has 29 events.
2026-04-09 12:16:08 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {}, targets: ['flows_provider'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.extract.slots        action_extract_slot=action_extract_slots len_extraction_events=0 rasa_events=[]
2026-04-09 12:16:08 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e)}, targets: ['command_processor'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=CommandProcessorComponent fn=execute_commands node_name=command_processor
2026-04-09 12:16:08 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] command_processor.clean_up_commands.skip_command_flow_already_active command=StartFlowCommand(flow='confirm_booking')
2026-04-09 12:16:08 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] command_processor.clean_up_commands.final_commands command=[SetSlotCommand(name='guest_count', value='160', extractor='LLM')]
2026-04-09 12:16:08 DEBUG    rasa.dialogue_understanding.commands.set_slot_command  - [debug    ] set_slot_command.set_slot      command=SetSlotCommand(name='guest_count', value='160', extractor='LLM')
2026-04-09 12:16:08 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_4_action_listen
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_4_action_listen flow_id=pattern_collect_information next_id=start
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_0_collect_guest_count', 'collect': 'guest_count', 'utter': 'utter_ask_guest_count', 'collect_action': 'action_ask_guest_count', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=start
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:08 DEBUG    rasa.core.policies.ensemble  - Made prediction using user intent.
2026-04-09 12:16:08 DEBUG    rasa.core.policies.ensemble  - Added `DefinePrevUserUtteredFeaturization(False)` event.
2026-04-09 12:16:08 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - Predicted next action 'action_run_slot_rejections' with confidence 1.00.
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_run_slot_rejections policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "start"}]"""), <rasa.shared.core.events.DefinePrevUserUtteredFeaturization object at 0x2965f8790>]
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_run_slot_rejections rasa_events=[]
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.slots.log            slots={'language': 'en', 'silence_timeout': 7.0, 'consecutive_silence_timeouts': 0.0, 'guest_count': 160.0, 'flow_hashes': {'confirm_booking': '0cfdd2e66537a1c1dc08453deb2ae383', 'handle_out_of_scope': '367e697b00b1da958c811004266f6c46', 'pattern_cancel_flow': '5edee5445ff87339ec899ab96de7ae9e', 'pattern_cannot_handle': '748dcc3783183f4c5512c2f23940b609', 'pattern_chitchat': 'aabaace3f5ef32b70351e18481c53356', 'pattern_clarification': '927f334af1fe5e570348690977bac4f2', 'pattern_code_change': 'f9db9f453c8b63fbec24c72413c86a69', 'pattern_collect_information': '072cd971740a761ddb8885f2cdc6ff20', 'pattern_completed': 'df3529f96e5d98df3f2ce63012daa641', 'pattern_continue_interrupted': '61bf7886bc116521c0d8f6f5b6760e67', 'pattern_correction': 'c35924757a8df574b91355c9a2070931', 'pattern_human_handoff': 'c021df067d37b8a23c464ca92372df6c', 'pattern_internal_error': 'b9059f3a7ca73e38b1d19ad0b09c9537', 'pattern_repeat_bot_messages': '35069cf740ceaff65ac467a58c3f77bf', 'pattern_restart': '9f4c81ddc0dcb8c4a74a141a047f0284', 'pattern_search': 'cf65ab2f7654f41f481a5f97cbcb9d9d', 'pattern_session_start': '757ea1cd44b685619e46d9c7b32c30b8', 'pattern_skip_question': '46505c0a24a5f90ab6f58a1fc69fa41b', 'pattern_user_silence': '41f05270eba1765c2fd9f1b17e1d754a', 'pattern_validate_slot': '57e5983e77f386ff93dfdcbad1c93308'}}
2026-04-09 12:16:08 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=start
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=start flow_id=pattern_collect_information next_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.predicate.evaluating      condition=slots.{{context.collect}} is not null flow_id=pattern_collect_information rendered_condition=slots.guest_count is not null
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.link.if_condition_satisfied current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information target=END
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information next_id=END
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=pattern_collect_information step_id=END
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=confirm_booking previous_step_id=confirm_booking_0_collect_guest_count
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=confirm_booking_0_collect_guest_count flow_id=confirm_booking next_id=confirm_booking_1_collect_vegan_count
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.collect          flow_id=confirm_booking step_id=confirm_booking_1_collect_vegan_count
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.reset_silence_timeout_to_global collect=vegan_count duration=7.0 flow_id=confirm_booking step_id=confirm_booking_1_collect_vegan_count
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=START
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=pattern_collect_information next_id=start
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_1_collect_vegan_count', 'collect': 'vegan_count', 'utter': 'utter_ask_vegan_count', 'collect_action': 'action_ask_vegan_count', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=start
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:08 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - Predicted next action 'action_run_slot_rejections' with confidence 1.00.
2026-04-09 12:16:08 DEBUG    rasa.core.actions.action_run_slot_rejections  - [debug    ] first.collect.slot.not.set     slot_name=vegan_count slot_value=None
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_run_slot_rejections policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_1_validate_{{context.collect}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/1"}]"""), FlowCompleted(flow: pattern_collect_information, step_id: pattern_collect_information_1_validate_{{context.collect}}), DialogueStackUpdate("""[{"op": "replace", "path": "/0/step_id", "value": "confirm_booking_1_collect_vegan_count"}]"""), DialogueStackUpdate("""[{"op": "add", "path": "/1", "value": {"frame_id": "D6SE7WK8", "flow_id": "pattern_collect_information", "step_id": "START", "collect": "vegan_count", "utter": "utter_ask_vegan_count", "collect_action": "action_ask_vegan_count", "rejections": [], "type": "pattern_collect_information"}}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "start"}]"""), FlowStarted(flow: pattern_collect_information)]
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_run_slot_rejections rasa_events=[]
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.slots.log            slots={'language': 'en', 'silence_timeout': 7.0, 'consecutive_silence_timeouts': 0.0, 'guest_count': 160.0, 'flow_hashes': {'confirm_booking': '0cfdd2e66537a1c1dc08453deb2ae383', 'handle_out_of_scope': '367e697b00b1da958c811004266f6c46', 'pattern_cancel_flow': '5edee5445ff87339ec899ab96de7ae9e', 'pattern_cannot_handle': '748dcc3783183f4c5512c2f23940b609', 'pattern_chitchat': 'aabaace3f5ef32b70351e18481c53356', 'pattern_clarification': '927f334af1fe5e570348690977bac4f2', 'pattern_code_change': 'f9db9f453c8b63fbec24c72413c86a69', 'pattern_collect_information': '072cd971740a761ddb8885f2cdc6ff20', 'pattern_completed': 'df3529f96e5d98df3f2ce63012daa641', 'pattern_continue_interrupted': '61bf7886bc116521c0d8f6f5b6760e67', 'pattern_correction': 'c35924757a8df574b91355c9a2070931', 'pattern_human_handoff': 'c021df067d37b8a23c464ca92372df6c', 'pattern_internal_error': 'b9059f3a7ca73e38b1d19ad0b09c9537', 'pattern_repeat_bot_messages': '35069cf740ceaff65ac467a58c3f77bf', 'pattern_restart': '9f4c81ddc0dcb8c4a74a141a047f0284', 'pattern_search': 'cf65ab2f7654f41f481a5f97cbcb9d9d', 'pattern_session_start': '757ea1cd44b685619e46d9c7b32c30b8', 'pattern_skip_question': '46505c0a24a5f90ab6f58a1fc69fa41b', 'pattern_user_silence': '41f05270eba1765c2fd9f1b17e1d754a', 'pattern_validate_slot': '57e5983e77f386ff93dfdcbad1c93308'}}
2026-04-09 12:16:08 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=start
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=start flow_id=pattern_collect_information next_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.predicate.evaluating      condition=slots.{{context.collect}} is not null flow_id=pattern_collect_information rendered_condition=slots.vegan_count is not null
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.link.else_condition_satisfied current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information target=ask_collect
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information next_id=ask_collect
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_1_collect_vegan_count', 'collect': 'vegan_count', 'utter': 'utter_ask_vegan_count', 'collect_action': 'action_ask_vegan_count', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=ask_collect
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:08 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - Predicted next action 'utter_ask_vegan_count' with confidence 1.00.
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_ask_vegan_count policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_1_validate_{{context.collect}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "ask_collect"}]""")]
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_ask_vegan_count rasa_events=[BotUttered('And how many of those guests will need vegan meals?', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"active_flow": "confirm_booking", "step_id": "confirm_booking_1_collect_vegan_count", "utter_action": "utter_ask_vegan_count", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733368.703252)]
2026-04-09 12:16:08 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=ask_collect
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=ask_collect flow_id=pattern_collect_information next_id=pattern_collect_information_3_{{context.collect_action}}
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_3_{{context.collect_action}}
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_3_{{context.collect_action}} flow_id=pattern_collect_information next_id=pattern_collect_information_4_action_listen
2026-04-09 12:16:08 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_1_collect_vegan_count', 'collect': 'vegan_count', 'utter': 'utter_ask_vegan_count', 'collect_action': 'action_ask_vegan_count', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=pattern_collect_information_4_action_listen
2026-04-09 12:16:08 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:08 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - Predicted next action 'action_listen' with confidence 1.00.
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_listen policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_3_{{context.collect_action}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_4_action_listen"}]""")]
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_listen rasa_events=[]
2026-04-09 12:16:08 DEBUG    rasa.core.tracker_stores.tracker_store  - [debug    ] No event broker configured. Skipping streaming events. event_key=tracker_store.stream_events.no_broker_configured
2026-04-09 12:16:08 DEBUG    rasa.core.processor  - [debug    ] processor.trigger_anonymization.skipping.pii_management_not_enabled
2026-04-09 12:16:08 DEBUG    rasa.core.lock_store  - [debug    ] Deleted lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._deleted_lock_for_conversation
And how many of those guests will need vegan meals?
Your input ->  50 vegan                                                                                                                                                     
2026-04-09 12:16:14 DEBUG    rasa.core.lock_store  - [debug    ] Issuing ticket for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store.issue_ticket
2026-04-09 12:16:14 DEBUG    rasa.core.lock_store  - [debug    ] Acquiring lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._acquiring_lock_for_conversation
2026-04-09 12:16:14 DEBUG    rasa.core.lock_store  - [debug    ] Acquired lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._acquired_lock_for_conversation
2026-04-09 12:16:14 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {}, targets: ['flows_provider'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__message__': [UserMessage(text: 50 vegan, sender_id: a8e9d54b848e4ab4ab08d70f1779476e)], '__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e)}, targets: ['run_RegexMessageHandler'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=NLUMessageConverter fn=convert_user_message node_name=nlu_message_converter
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=CompactLLMCommandGenerator fn=process node_name=run_CompactLLMCommandGenerator0
2026-04-09 12:16:14 DEBUG    rasa.dialogue_understanding.utils  - [debug    ] Tracker doesn't have the 'route_session_to_calm' slot.Routing to CALM. event_key=utils.handle_via_nlu_in_coexistence.tracker_missing_route_session_to_calm_slot route_session_to_calm=[]
2026-04-09 12:16:14 DEBUG    rasa.shared.providers.embedding._base_litellm_embedding_client  - [debug    ] base_litellm_client.formatted_response formatted_response={'data': 'Embedding response data not shown here for brevity.', 'model': 'Qwen/Qwen3-Embedding-8B', 'usage': {'prompt_tokens': 2, 'completion_tokens': 0, 'total_tokens': 2}, 'additional_info': None}

Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers


Provider List: https://docs.litellm.ai/docs/providers

2026-04-09 12:16:14 DEBUG    rasa.dialogue_understanding.generator.flow_retrieval  - [debug    ] Fetched the top 20similar flows from the vector store event_key=flow_retrieval.query_vector_store.fetched query=50 vegan results=[{'flow_id': 'confirm_booking', 'score': 0.55938935, 'content': "confirm booking: Handle an inbound call from a pub manager confirming a venue booking for tonight's event. Triggered when the pub manager calls to confirm booking details, including guest count, dietary requirements, and deposit terms. This is the primary task — all booking-related calls should use this flow.\n\n    guest_count: total number of guests attending tonight's event\n    vegan_count: number of guests requiring vegan meals\n    deposit_amount_gbp: deposit amount in GBP the manager is proposing to secure the booking"}, {'flow_id': 'handle_out_of_scope', 'score': 0.45960027, 'content': 'handle out of scope: Handle requests that are outside the scope of booking confirmation, such as questions about parking, AV equipment, seating arrangements, menus, weather, or any non-booking topic.'}] top_k=20
2026-04-09 12:16:14 DEBUG    rasa.dialogue_understanding.generator.llm_based_command_generator  - [debug    ] llm_based_command_generator.predict_commands.filtered_flows enabled_flow_retrieval=True message={'text': '50 vegan', 'message_id': 'c9a68e0bb8a14a1caf4a3a4717b4a169', 'metadata': None, 'flows_from_semantic_search': [('confirm_booking', 0.5593893527984619), ('handle_out_of_scope', 0.4596002697944641)], 'flows_in_prompt': ['confirm_booking', 'handle_out_of_scope']} relevant_flows=['confirm_booking', 'handle_out_of_scope']
2026-04-09 12:16:14 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.prompt_rendered prompt=## Task Description
Your task is to analyze the current conversation context and generate a list of actions to start new business processes that we call flows, to extract slots, or respond to small talk and knowledge requests.

---

## Available Flows and Slots
Use the following structured data:
```json
{"flows":[{"name":"confirm_booking","description":"Handle an inbound call from a pub manager confirming a venue booking for tonight's event. Triggered when the pub manager calls to confirm booking details, including guest count, dietary requirements, and deposit terms. This is the primary task — all booking-related calls should use this flow.\n","slots":[{"name":"guest_count","description":"total number of guests attending tonight's event"},{"name":"vegan_count","description":"number of guests requiring vegan meals"},{"name":"deposit_amount_gbp","description":"deposit amount in GBP the manager is proposing to secure the booking"}]},{"name":"handle_out_of_scope","description":"Handle requests that are outside the scope of booking confirmation, such as questions about parking, AV equipment, seating arrangements, menus, weather, or any non-booking topic.\n"}]}
```

---

## Available Actions:
* `start flow flow_name`: Starting a flow. For example, `start flow transfer_money` or `start flow list_contacts`.
* `set slot slot_name slot_value`: Slot setting. For example, `set slot transfer_money_recipient Freddy`. Can be used to correct and change previously set values.
* `cancel flow`: Cancelling the current flow.
* `disambiguate flows flow_name1 flow_name2 ... flow_name_n`: Disambiguate which flow should be started when user input is ambiguous by listing the potential flows as options. For example, `disambiguate flows list_contacts add_contact remove_contact ...` if the user just wrote "contacts".
* `provide info`: Responding to the user's questions by supplying relevant information, such as answering FAQs or explaining services.
* `offtopic reply`: Responding to casual or social user messages that are unrelated to any flows, engaging in friendly conversation and addressing off-topic remarks.
* `hand over`: Handing over to a human, in case the user seems frustrated or explicitly asks to speak to one.
* `repeat message`: Repeating the last bot message.

---

## General Tips
* Do not fill slots with abstract values or placeholders.
* For categorical slots try to match the user message with allowed slot values. Use "other" if you cannot match it.
* Set the boolean slots based on the user response. Map positive responses to `True`, and negative to `False`.
* Extract text slot values exactly as provided by the user. Avoid assumptions, format changes, or partial extractions.
* Only use information provided by the user.
* Use clarification in ambiguous cases.
* Multiple flows can be started. If a user wants to digress into a second flow, you do not need to cancel the current flow.
* Do not cancel the flow unless the user explicitly requests it.
* Strictly adhere to the provided action format.
* Focus on the last message and take it one step at a time.
* Use the previous conversation steps only to aid understanding.

---

## Current State
Use the following structured data:
```json
{"active_flow":"confirm_booking","current_step":{"requested_slot":"vegan_count","requested_slot_description":"number of guests requiring vegan meals"},"slots":[{"name":"guest_count","value":"160.0","type":"float","description":"total number of guests attending tonight's event"},{"name":"vegan_count","value":"undefined","type":"float","description":"number of guests requiring vegan meals"},{"name":"deposit_amount_gbp","value":"undefined","type":"float","description":"deposit amount in GBP the manager is proposing to secure the booking"}]}
```

---

## Conversation History
USER: calling to confirm a booking
AI: I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
AI: How many guests are you confirming for tonight's event?
USER: 160 guests
AI: And how many of those guests will need vegan meals?
USER: 50 vegan

---

## Task
Create an action list with one action per line in response to the user's last message: """50 vegan""".

Your action list:
/Users/mihalis/PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:390: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='1. set slot vegan_count 50\n2. pr...unction_call=None, provider_specific_fields=None)` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...ider_specific_fields={})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_python(
2026-04-09 12:16:14 DEBUG    rasa.shared.providers.llm._base_litellm_client  - [debug    ] base_litellm_client.formatted_response formatted_response={'id': 'chatcmpl-486362e2638f4a7fa4a14e1527706203', 'choices': ['1. set slot vegan_count 50\n2. provide info'], 'created': 1775682937, 'model': 'hosted_vllm/meta-llama/Llama-3.3-70B-Instruct', 'usage': {'prompt_tokens': 920, 'completion_tokens': 14, 'total_tokens': 934}, 'additional_info': None, 'latency': None}
2026-04-09 12:16:14 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.actions_generated action_list=1. set slot vegan_count 50
2. provide info
2026-04-09 12:16:14 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.finished commands=[SetSlotCommand(name='vegan_count', value='50', extractor='LLM'), KnowledgeAnswerCommand()]
2026-04-09 12:16:14 DEBUG    rasa.dialogue_understanding.generator.llm_based_command_generator  - [debug    ] command_processor.check_commands_against_slot_mappings.active_flow active_flow=confirm_booking
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RegexMessageHandler fn=process node_name=run_RegexMessageHandler
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.message.parse        parse_data_entities=[] parse_data_intent={'name': None, 'confidence': 0.0} parse_data_text=50 vegan
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - Logged UserUtterance - tracker now has 50 events.
2026-04-09 12:16:14 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {}, targets: ['flows_provider'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.extract.slots        action_extract_slot=action_extract_slots len_extraction_events=0 rasa_events=[]
2026-04-09 12:16:14 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e)}, targets: ['command_processor'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=CommandProcessorComponent fn=execute_commands node_name=command_processor
2026-04-09 12:16:14 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] command_processor.clean_up_commands.prepend_command_freeform_answer command=KnowledgeAnswerCommand()
2026-04-09 12:16:14 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] command_processor.clean_up_commands.final_commands command=[KnowledgeAnswerCommand(), SetSlotCommand(name='vegan_count', value='50', extractor='LLM')]
2026-04-09 12:16:14 DEBUG    rasa.dialogue_understanding.commands.set_slot_command  - [debug    ] set_slot_command.set_slot      command=SetSlotCommand(name='vegan_count', value='50', extractor='LLM')
2026-04-09 12:16:14 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_search previous_step_id=START
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=pattern_search next_id=pattern_search_0_utter_no_knowledge_base
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'CSU5AAU5', 'flow_id': 'pattern_search', 'step_id': 'pattern_search_0_utter_no_knowledge_base', 'type': 'pattern_search'}} flow_id=pattern_search step_id=pattern_search_0_utter_no_knowledge_base
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:14 DEBUG    rasa.core.policies.ensemble  - Made prediction using user intent.
2026-04-09 12:16:14 DEBUG    rasa.core.policies.ensemble  - Added `DefinePrevUserUtteredFeaturization(False)` event.
2026-04-09 12:16:14 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - Predicted next action 'utter_no_knowledge_base' with confidence 1.00.
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_no_knowledge_base policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "pattern_search_0_utter_no_knowledge_base"}]"""), FlowStarted(flow: pattern_search), <rasa.shared.core.events.DefinePrevUserUtteredFeaturization object at 0x2966fee00>]
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_no_knowledge_base rasa_events=[BotUttered('I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"metadata": {"rephrase": true}, "active_flow": "pattern_search", "step_id": "pattern_search_0_utter_no_knowledge_base", "utter_action": "utter_no_knowledge_base", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733374.842772)]
2026-04-09 12:16:14 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_search previous_step_id=pattern_search_0_utter_no_knowledge_base
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_search_0_utter_no_knowledge_base flow_id=pattern_search next_id=END
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=pattern_search step_id=END
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_4_action_listen
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_4_action_listen flow_id=pattern_collect_information next_id=start
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_1_collect_vegan_count', 'collect': 'vegan_count', 'utter': 'utter_ask_vegan_count', 'collect_action': 'action_ask_vegan_count', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=start
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:14 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - Predicted next action 'action_run_slot_rejections' with confidence 1.00.
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_run_slot_rejections policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/2"}]"""), FlowCompleted(flow: pattern_search, step_id: pattern_search_0_utter_no_knowledge_base), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "start"}]""")]
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_run_slot_rejections rasa_events=[]
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.slots.log            slots={'language': 'en', 'silence_timeout': 7.0, 'consecutive_silence_timeouts': 0.0, 'guest_count': 160.0, 'vegan_count': 50.0, 'flow_hashes': {'confirm_booking': '0cfdd2e66537a1c1dc08453deb2ae383', 'handle_out_of_scope': '367e697b00b1da958c811004266f6c46', 'pattern_cancel_flow': '5edee5445ff87339ec899ab96de7ae9e', 'pattern_cannot_handle': '748dcc3783183f4c5512c2f23940b609', 'pattern_chitchat': 'aabaace3f5ef32b70351e18481c53356', 'pattern_clarification': '927f334af1fe5e570348690977bac4f2', 'pattern_code_change': 'f9db9f453c8b63fbec24c72413c86a69', 'pattern_collect_information': '072cd971740a761ddb8885f2cdc6ff20', 'pattern_completed': 'df3529f96e5d98df3f2ce63012daa641', 'pattern_continue_interrupted': '61bf7886bc116521c0d8f6f5b6760e67', 'pattern_correction': 'c35924757a8df574b91355c9a2070931', 'pattern_human_handoff': 'c021df067d37b8a23c464ca92372df6c', 'pattern_internal_error': 'b9059f3a7ca73e38b1d19ad0b09c9537', 'pattern_repeat_bot_messages': '35069cf740ceaff65ac467a58c3f77bf', 'pattern_restart': '9f4c81ddc0dcb8c4a74a141a047f0284', 'pattern_search': 'cf65ab2f7654f41f481a5f97cbcb9d9d', 'pattern_session_start': '757ea1cd44b685619e46d9c7b32c30b8', 'pattern_skip_question': '46505c0a24a5f90ab6f58a1fc69fa41b', 'pattern_user_silence': '41f05270eba1765c2fd9f1b17e1d754a', 'pattern_validate_slot': '57e5983e77f386ff93dfdcbad1c93308'}}
2026-04-09 12:16:14 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=start
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=start flow_id=pattern_collect_information next_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.predicate.evaluating      condition=slots.{{context.collect}} is not null flow_id=pattern_collect_information rendered_condition=slots.vegan_count is not null
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.link.if_condition_satisfied current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information target=END
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information next_id=END
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=pattern_collect_information step_id=END
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=confirm_booking previous_step_id=confirm_booking_1_collect_vegan_count
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=confirm_booking_1_collect_vegan_count flow_id=confirm_booking next_id=confirm_booking_2_collect_deposit_amount_gbp
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.collect          flow_id=confirm_booking step_id=confirm_booking_2_collect_deposit_amount_gbp
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.reset_silence_timeout_to_global collect=deposit_amount_gbp duration=7.0 flow_id=confirm_booking step_id=confirm_booking_2_collect_deposit_amount_gbp
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=START
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=pattern_collect_information next_id=start
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_2_collect_deposit_amount_gbp', 'collect': 'deposit_amount_gbp', 'utter': 'utter_ask_deposit_amount_gbp', 'collect_action': 'action_ask_deposit_amount_gbp', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=start
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:14 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - Predicted next action 'action_run_slot_rejections' with confidence 1.00.
2026-04-09 12:16:14 DEBUG    rasa.core.actions.action_run_slot_rejections  - [debug    ] first.collect.slot.not.set     slot_name=deposit_amount_gbp slot_value=None
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_run_slot_rejections policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_1_validate_{{context.collect}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/1"}]"""), FlowCompleted(flow: pattern_collect_information, step_id: pattern_collect_information_1_validate_{{context.collect}}), DialogueStackUpdate("""[{"op": "replace", "path": "/0/step_id", "value": "confirm_booking_2_collect_deposit_amount_gbp"}]"""), DialogueStackUpdate("""[{"op": "add", "path": "/1", "value": {"frame_id": "737M34YL", "flow_id": "pattern_collect_information", "step_id": "START", "collect": "deposit_amount_gbp", "utter": "utter_ask_deposit_amount_gbp", "collect_action": "action_ask_deposit_amount_gbp", "rejections": [], "type": "pattern_collect_information"}}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "start"}]"""), FlowStarted(flow: pattern_collect_information)]
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_run_slot_rejections rasa_events=[]
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.slots.log            slots={'language': 'en', 'silence_timeout': 7.0, 'consecutive_silence_timeouts': 0.0, 'guest_count': 160.0, 'vegan_count': 50.0, 'flow_hashes': {'confirm_booking': '0cfdd2e66537a1c1dc08453deb2ae383', 'handle_out_of_scope': '367e697b00b1da958c811004266f6c46', 'pattern_cancel_flow': '5edee5445ff87339ec899ab96de7ae9e', 'pattern_cannot_handle': '748dcc3783183f4c5512c2f23940b609', 'pattern_chitchat': 'aabaace3f5ef32b70351e18481c53356', 'pattern_clarification': '927f334af1fe5e570348690977bac4f2', 'pattern_code_change': 'f9db9f453c8b63fbec24c72413c86a69', 'pattern_collect_information': '072cd971740a761ddb8885f2cdc6ff20', 'pattern_completed': 'df3529f96e5d98df3f2ce63012daa641', 'pattern_continue_interrupted': '61bf7886bc116521c0d8f6f5b6760e67', 'pattern_correction': 'c35924757a8df574b91355c9a2070931', 'pattern_human_handoff': 'c021df067d37b8a23c464ca92372df6c', 'pattern_internal_error': 'b9059f3a7ca73e38b1d19ad0b09c9537', 'pattern_repeat_bot_messages': '35069cf740ceaff65ac467a58c3f77bf', 'pattern_restart': '9f4c81ddc0dcb8c4a74a141a047f0284', 'pattern_search': 'cf65ab2f7654f41f481a5f97cbcb9d9d', 'pattern_session_start': '757ea1cd44b685619e46d9c7b32c30b8', 'pattern_skip_question': '46505c0a24a5f90ab6f58a1fc69fa41b', 'pattern_user_silence': '41f05270eba1765c2fd9f1b17e1d754a', 'pattern_validate_slot': '57e5983e77f386ff93dfdcbad1c93308'}}
2026-04-09 12:16:14 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=start
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=start flow_id=pattern_collect_information next_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.predicate.evaluating      condition=slots.{{context.collect}} is not null flow_id=pattern_collect_information rendered_condition=slots.deposit_amount_gbp is not null
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.link.else_condition_satisfied current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information target=ask_collect
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information next_id=ask_collect
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_2_collect_deposit_amount_gbp', 'collect': 'deposit_amount_gbp', 'utter': 'utter_ask_deposit_amount_gbp', 'collect_action': 'action_ask_deposit_amount_gbp', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=ask_collect
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:14 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - Predicted next action 'utter_ask_deposit_amount_gbp' with confidence 1.00.
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_ask_deposit_amount_gbp policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_1_validate_{{context.collect}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "ask_collect"}]""")]
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_ask_deposit_amount_gbp rasa_events=[BotUttered('What deposit amount in GBP are you proposing to secure the booking?', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"active_flow": "confirm_booking", "step_id": "confirm_booking_2_collect_deposit_amount_gbp", "utter_action": "utter_ask_deposit_amount_gbp", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733374.867636)]
2026-04-09 12:16:14 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=ask_collect
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=ask_collect flow_id=pattern_collect_information next_id=pattern_collect_information_3_{{context.collect_action}}
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_3_{{context.collect_action}}
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_3_{{context.collect_action}} flow_id=pattern_collect_information next_id=pattern_collect_information_4_action_listen
2026-04-09 12:16:14 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_2_collect_deposit_amount_gbp', 'collect': 'deposit_amount_gbp', 'utter': 'utter_ask_deposit_amount_gbp', 'collect_action': 'action_ask_deposit_amount_gbp', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=pattern_collect_information_4_action_listen
I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
2026-04-09 12:16:14 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:14 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - Predicted next action 'action_listen' with confidence 1.00.
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_listen policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_3_{{context.collect_action}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_4_action_listen"}]""")]
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_listen rasa_events=[]
2026-04-09 12:16:14 DEBUG    rasa.core.tracker_stores.tracker_store  - [debug    ] No event broker configured. Skipping streaming events. event_key=tracker_store.stream_events.no_broker_configured
2026-04-09 12:16:14 DEBUG    rasa.core.processor  - [debug    ] processor.trigger_anonymization.skipping.pii_management_not_enabled
2026-04-09 12:16:14 DEBUG    rasa.core.lock_store  - [debug    ] Deleted lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._deleted_lock_for_conversation
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  can you arrange parking for the customers?                                                                                                                   
2026-04-09 12:16:43 DEBUG    rasa.core.lock_store  - [debug    ] Issuing ticket for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store.issue_ticket
2026-04-09 12:16:43 DEBUG    rasa.core.lock_store  - [debug    ] Acquiring lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._acquiring_lock_for_conversation
2026-04-09 12:16:43 DEBUG    rasa.core.lock_store  - [debug    ] Acquired lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._acquired_lock_for_conversation
2026-04-09 12:16:43 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {}, targets: ['flows_provider'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:43 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__message__': [UserMessage(text: can you arrange parking for the customers?, sender_id: a8e9d54b848e4ab4ab08d70f1779476e)], '__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e)}, targets: ['run_RegexMessageHandler'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=NLUMessageConverter fn=convert_user_message node_name=nlu_message_converter
2026-04-09 12:16:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=CompactLLMCommandGenerator fn=process node_name=run_CompactLLMCommandGenerator0
2026-04-09 12:16:43 DEBUG    rasa.dialogue_understanding.utils  - [debug    ] Tracker doesn't have the 'route_session_to_calm' slot.Routing to CALM. event_key=utils.handle_via_nlu_in_coexistence.tracker_missing_route_session_to_calm_slot route_session_to_calm=[]
2026-04-09 12:16:43 DEBUG    rasa.shared.providers.embedding._base_litellm_embedding_client  - [debug    ] base_litellm_client.formatted_response formatted_response={'data': 'Embedding response data not shown here for brevity.', 'model': 'Qwen/Qwen3-Embedding-8B', 'usage': {'prompt_tokens': 9, 'completion_tokens': 0, 'total_tokens': 9}, 'additional_info': None}
2026-04-09 12:16:43 DEBUG    rasa.dialogue_understanding.generator.flow_retrieval  - [debug    ] Fetched the top 20similar flows from the vector store event_key=flow_retrieval.query_vector_store.fetched query=can you arrange parking for the customers? results=[{'flow_id': 'handle_out_of_scope', 'score': 0.6976665, 'content': 'handle out of scope: Handle requests that are outside the scope of booking confirmation, such as questions about parking, AV equipment, seating arrangements, menus, weather, or any non-booking topic.'}, {'flow_id': 'confirm_booking', 'score': 0.64921445, 'content': "confirm booking: Handle an inbound call from a pub manager confirming a venue booking for tonight's event. Triggered when the pub manager calls to confirm booking details, including guest count, dietary requirements, and deposit terms. This is the primary task — all booking-related calls should use this flow.\n\n    guest_count: total number of guests attending tonight's event\n    vegan_count: number of guests requiring vegan meals\n    deposit_amount_gbp: deposit amount in GBP the manager is proposing to secure the booking"}] top_k=20
2026-04-09 12:16:43 DEBUG    rasa.dialogue_understanding.generator.llm_based_command_generator  - [debug    ] llm_based_command_generator.predict_commands.filtered_flows enabled_flow_retrieval=True message={'text': 'can you arrange parking for the customers?', 'message_id': '78df73bbbd754783afea87bb9c0379f1', 'metadata': None, 'flows_from_semantic_search': [('handle_out_of_scope', 0.6976665258407593), ('confirm_booking', 0.6492144465446472)], 'flows_in_prompt': ['confirm_booking', 'handle_out_of_scope']} relevant_flows=['confirm_booking', 'handle_out_of_scope']
2026-04-09 12:16:43 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.prompt_rendered prompt=## Task Description
Your task is to analyze the current conversation context and generate a list of actions to start new business processes that we call flows, to extract slots, or respond to small talk and knowledge requests.

---

## Available Flows and Slots
Use the following structured data:
```json
{"flows":[{"name":"confirm_booking","description":"Handle an inbound call from a pub manager confirming a venue booking for tonight's event. Triggered when the pub manager calls to confirm booking details, including guest count, dietary requirements, and deposit terms. This is the primary task — all booking-related calls should use this flow.\n","slots":[{"name":"guest_count","description":"total number of guests attending tonight's event"},{"name":"vegan_count","description":"number of guests requiring vegan meals"},{"name":"deposit_amount_gbp","description":"deposit amount in GBP the manager is proposing to secure the booking"}]},{"name":"handle_out_of_scope","description":"Handle requests that are outside the scope of booking confirmation, such as questions about parking, AV equipment, seating arrangements, menus, weather, or any non-booking topic.\n"}]}
```

---

## Available Actions:
* `start flow flow_name`: Starting a flow. For example, `start flow transfer_money` or `start flow list_contacts`.
* `set slot slot_name slot_value`: Slot setting. For example, `set slot transfer_money_recipient Freddy`. Can be used to correct and change previously set values.
* `cancel flow`: Cancelling the current flow.
* `disambiguate flows flow_name1 flow_name2 ... flow_name_n`: Disambiguate which flow should be started when user input is ambiguous by listing the potential flows as options. For example, `disambiguate flows list_contacts add_contact remove_contact ...` if the user just wrote "contacts".
* `provide info`: Responding to the user's questions by supplying relevant information, such as answering FAQs or explaining services.
* `offtopic reply`: Responding to casual or social user messages that are unrelated to any flows, engaging in friendly conversation and addressing off-topic remarks.
* `hand over`: Handing over to a human, in case the user seems frustrated or explicitly asks to speak to one.
* `repeat message`: Repeating the last bot message.

---

## General Tips
* Do not fill slots with abstract values or placeholders.
* For categorical slots try to match the user message with allowed slot values. Use "other" if you cannot match it.
* Set the boolean slots based on the user response. Map positive responses to `True`, and negative to `False`.
* Extract text slot values exactly as provided by the user. Avoid assumptions, format changes, or partial extractions.
* Only use information provided by the user.
* Use clarification in ambiguous cases.
* Multiple flows can be started. If a user wants to digress into a second flow, you do not need to cancel the current flow.
* Do not cancel the flow unless the user explicitly requests it.
* Strictly adhere to the provided action format.
* Focus on the last message and take it one step at a time.
* Use the previous conversation steps only to aid understanding.

---

## Current State
Use the following structured data:
```json
{"active_flow":"confirm_booking","current_step":{"requested_slot":"deposit_amount_gbp","requested_slot_description":"deposit amount in GBP the manager is proposing to secure the booking"},"slots":[{"name":"guest_count","value":"160.0","type":"float","description":"total number of guests attending tonight's event"},{"name":"vegan_count","value":"50.0","type":"float","description":"number of guests requiring vegan meals"},{"name":"deposit_amount_gbp","value":"undefined","type":"float","description":"deposit amount in GBP the manager is proposing to secure the booking"}]}
```

---

## Conversation History
USER: calling to confirm a booking
AI: I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
AI: How many guests are you confirming for tonight's event?
USER: 160 guests
AI: And how many of those guests will need vegan meals?
USER: 50 vegan
AI: I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
AI: What deposit amount in GBP are you proposing to secure the booking?
USER: can you arrange parking for the customers?

---

## Task
Create an action list with one action per line in response to the user's last message: 
"""
"""Your action list:
/Users//PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:441: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='start flow handle_out_of_scope \n...None, provider_specific_fields={'refusal': None})` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...one, 'token_ids': None})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_json(
2026-04-09 12:16:44 DEBUG    rasa.shared.providers.llm._base_litellm_client  - [debug    ] base_litellm_client.formatted_response formatted_response={'id': 'chatcmpl-dde46f34d61a406f8e50bccdc0a8ada5', 'choices': ['start flow handle_out_of_scope \nofftopic reply \nprovide info'], 'created': 1775733404, 'model': 'hosted_vllm/meta-llama/Llama-3.3-70B-Instruct', 'usage': {'prompt_tokens': 987, 'completion_tokens': 14, 'total_tokens': 1001}, 'additional_info': None, 'latency': None}
2026-04-09 12:16:44 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.actions_generated action_list=start flow handle_out_of_scope
offtopic reply
provide info
2026-04-09 12:16:44 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.finished commands=[StartFlowCommand(flow='handle_out_of_scope'), ChitChatAnswerCommand(), KnowledgeAnswerCommand()]
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RegexMessageHandler fn=process node_name=run_RegexMessageHandler
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.message.parse        parse_data_entities=[] parse_data_intent={'name': None, 'confidence': 0.0} parse_data_text=can you arrange parking for the customers?
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - Logged UserUtterance - tracker now has 79 events.
2026-04-09 12:16:44 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {}, targets: ['flows_provider'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.extract.slots        action_extract_slot=action_extract_slots len_extraction_events=0 rasa_events=[]
2026-04-09 12:16:44 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e)}, targets: ['command_processor'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=CommandProcessorComponent fn=execute_commands node_name=command_processor
2026-04-09 12:16:44 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] command_processor.clean_up_commands.prepend_command_chitchat_answer command=ChitChatAnswerCommand() defined_intentless_policy_in_config=False pattern_chitchat_uses_action_trigger_chitchat=False
2026-04-09 12:16:44 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] command_processor.clean_up_commands.prepend_command_freeform_answer command=KnowledgeAnswerCommand()
2026-04-09 12:16:44 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] command_processor.clean_up_commands.final_commands command=[KnowledgeAnswerCommand(), ChitChatAnswerCommand(), StartFlowCommand(flow='handle_out_of_scope')]
2026-04-09 12:16:44 DEBUG    rasa.dialogue_understanding.commands.start_flow_command  - [debug    ] start_flow_command.start_flow  command=StartFlowCommand(flow='handle_out_of_scope')
2026-04-09 12:16:44 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_search previous_step_id=START
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=pattern_search next_id=pattern_search_0_utter_no_knowledge_base
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'WD9YJG0S', 'flow_id': 'pattern_search', 'step_id': 'pattern_search_0_utter_no_knowledge_base', 'type': 'pattern_search'}} flow_id=pattern_search step_id=pattern_search_0_utter_no_knowledge_base
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:44 DEBUG    rasa.core.policies.ensemble  - Made prediction using user intent.
2026-04-09 12:16:44 DEBUG    rasa.core.policies.ensemble  - Added `DefinePrevUserUtteredFeaturization(False)` event.
2026-04-09 12:16:44 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - Predicted next action 'utter_no_knowledge_base' with confidence 1.00.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_no_knowledge_base policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/4/step_id", "value": "pattern_search_0_utter_no_knowledge_base"}]"""), FlowStarted(flow: pattern_search), <rasa.shared.core.events.DefinePrevUserUtteredFeaturization object at 0x2970ded10>]
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_no_knowledge_base rasa_events=[BotUttered('I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"metadata": {"rephrase": true}, "active_flow": "pattern_search", "step_id": "pattern_search_0_utter_no_knowledge_base", "utter_action": "utter_no_knowledge_base", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733404.911694)]
2026-04-09 12:16:44 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_search previous_step_id=pattern_search_0_utter_no_knowledge_base
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_search_0_utter_no_knowledge_base flow_id=pattern_search next_id=END
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=pattern_search step_id=END
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_chitchat previous_step_id=START
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=pattern_chitchat next_id=pattern_chitchat_0_utter_cannot_handle
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'L6MVYD3T', 'flow_id': 'pattern_chitchat', 'step_id': 'pattern_chitchat_0_utter_cannot_handle', 'type': 'pattern_chitchat'}} flow_id=pattern_chitchat step_id=pattern_chitchat_0_utter_cannot_handle
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:44 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - Predicted next action 'utter_cannot_handle' with confidence 1.00.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_cannot_handle policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/4/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/4"}]"""), FlowCompleted(flow: pattern_search, step_id: pattern_search_0_utter_no_knowledge_base), DialogueStackUpdate("""[{"op": "replace", "path": "/3/step_id", "value": "pattern_chitchat_0_utter_cannot_handle"}]"""), FlowStarted(flow: pattern_chitchat)]
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_cannot_handle rasa_events=[BotUttered('I'm sorry, I'm not trained to help with that.', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"active_flow": "pattern_chitchat", "step_id": "pattern_chitchat_0_utter_cannot_handle", "utter_action": "utter_cannot_handle", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733404.923258)]
2026-04-09 12:16:44 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_chitchat previous_step_id=pattern_chitchat_0_utter_cannot_handle
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_chitchat_0_utter_cannot_handle flow_id=pattern_chitchat next_id=END
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=pattern_chitchat step_id=END
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=handle_out_of_scope previous_step_id=START
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=handle_out_of_scope next_id=handle_out_of_scope_0_utter_out_of_scope
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'FXALX30R', 'flow_id': 'handle_out_of_scope', 'step_id': 'handle_out_of_scope_0_utter_out_of_scope', 'frame_type': 'interrupt', 'type': 'flow'}} flow_id=handle_out_of_scope step_id=handle_out_of_scope_0_utter_out_of_scope
I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:44 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - Predicted next action 'utter_out_of_scope' with confidence 1.00.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_out_of_scope policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/3/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/3"}]"""), FlowCompleted(flow: pattern_chitchat, step_id: pattern_chitchat_0_utter_cannot_handle), DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "handle_out_of_scope_0_utter_out_of_scope"}]"""), FlowStarted(flow: handle_out_of_scope)]
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_out_of_scope rasa_events=[BotUttered('I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"active_flow": "handle_out_of_scope", "step_id": "handle_out_of_scope_0_utter_out_of_scope", "utter_action": "utter_out_of_scope", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733404.932728)]
2026-04-09 12:16:44 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=handle_out_of_scope previous_step_id=handle_out_of_scope_0_utter_out_of_scope
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=handle_out_of_scope_0_utter_out_of_scope flow_id=handle_out_of_scope next_id=END
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=handle_out_of_scope step_id=END
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_continue_interrupted previous_step_id=START
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=pattern_continue_interrupted next_id=pattern_continue_interrupted_0_utter_flow_continue_interrupted
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'HTQ8TKOD', 'flow_id': 'pattern_continue_interrupted', 'step_id': 'pattern_continue_interrupted_0_utter_flow_continue_interrupted', 'previous_flow_name': 'confirm booking', 'type': 'pattern_continue_interrupted'}} flow_id=pattern_continue_interrupted step_id=pattern_continue_interrupted_0_utter_flow_continue_interrupted
I'm sorry, I'm not trained to help with that.
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:44 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - Predicted next action 'utter_flow_continue_interrupted' with confidence 1.00.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_flow_continue_interrupted policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/2/frame_type"}, {"op": "add", "path": "/2/previous_flow_name", "value": "confirm booking"}, {"op": "replace", "path": "/2/step_id", "value": "START"}, {"op": "replace", "path": "/2/type", "value": "pattern_continue_interrupted"}, {"op": "replace", "path": "/2/frame_id", "value": "HTQ8TKOD"}, {"op": "replace", "path": "/2/flow_id", "value": "pattern_continue_interrupted"}]"""), FlowCompleted(flow: handle_out_of_scope, step_id: handle_out_of_scope_0_utter_out_of_scope), FlowResumed(flow: confirm_booking, step_id: confirm_booking_2_collect_deposit_amount_gbp), DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "pattern_continue_interrupted_0_utter_flow_continue_interrupted"}]"""), FlowStarted(flow: pattern_continue_interrupted)]
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_flow_continue_interrupted rasa_events=[BotUttered('Let's continue with confirm booking.', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"metadata": {"rephrase": true, "template": "jinja"}, "active_flow": "pattern_continue_interrupted", "step_id": "pattern_continue_interrupted_0_utter_flow_continue_interrupted", "utter_action": "utter_flow_continue_interrupted", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733404.942778)]
2026-04-09 12:16:44 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_continue_interrupted previous_step_id=pattern_continue_interrupted_0_utter_flow_continue_interrupted
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_continue_interrupted_0_utter_flow_continue_interrupted flow_id=pattern_continue_interrupted next_id=END
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=pattern_continue_interrupted step_id=END
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_4_action_listen
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_4_action_listen flow_id=pattern_collect_information next_id=start
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_2_collect_deposit_amount_gbp', 'collect': 'deposit_amount_gbp', 'utter': 'utter_ask_deposit_amount_gbp', 'collect_action': 'action_ask_deposit_amount_gbp', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=start
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:44 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - Predicted next action 'action_run_slot_rejections' with confidence 1.00.
2026-04-09 12:16:44 DEBUG    rasa.core.actions.action_run_slot_rejections  - [debug    ] first.collect.slot.not.set     slot_name=deposit_amount_gbp slot_value=None
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_run_slot_rejections policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/2"}]"""), FlowCompleted(flow: pattern_continue_interrupted, step_id: pattern_continue_interrupted_0_utter_flow_continue_interrupted), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "start"}]""")]
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_run_slot_rejections rasa_events=[]
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.slots.log            slots={'language': 'en', 'silence_timeout': 7.0, 'consecutive_silence_timeouts': 0.0, 'guest_count': 160.0, 'vegan_count': 50.0, 'flow_hashes': {'confirm_booking': '0cfdd2e66537a1c1dc08453deb2ae383', 'handle_out_of_scope': '367e697b00b1da958c811004266f6c46', 'pattern_cancel_flow': '5edee5445ff87339ec899ab96de7ae9e', 'pattern_cannot_handle': '748dcc3783183f4c5512c2f23940b609', 'pattern_chitchat': 'aabaace3f5ef32b70351e18481c53356', 'pattern_clarification': '927f334af1fe5e570348690977bac4f2', 'pattern_code_change': 'f9db9f453c8b63fbec24c72413c86a69', 'pattern_collect_information': '072cd971740a761ddb8885f2cdc6ff20', 'pattern_completed': 'df3529f96e5d98df3f2ce63012daa641', 'pattern_continue_interrupted': '61bf7886bc116521c0d8f6f5b6760e67', 'pattern_correction': 'c35924757a8df574b91355c9a2070931', 'pattern_human_handoff': 'c021df067d37b8a23c464ca92372df6c', 'pattern_internal_error': 'b9059f3a7ca73e38b1d19ad0b09c9537', 'pattern_repeat_bot_messages': '35069cf740ceaff65ac467a58c3f77bf', 'pattern_restart': '9f4c81ddc0dcb8c4a74a141a047f0284', 'pattern_search': 'cf65ab2f7654f41f481a5f97cbcb9d9d', 'pattern_session_start': '757ea1cd44b685619e46d9c7b32c30b8', 'pattern_skip_question': '46505c0a24a5f90ab6f58a1fc69fa41b', 'pattern_user_silence': '41f05270eba1765c2fd9f1b17e1d754a', 'pattern_validate_slot': '57e5983e77f386ff93dfdcbad1c93308'}}
2026-04-09 12:16:44 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=start
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=start flow_id=pattern_collect_information next_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.predicate.evaluating      condition=slots.{{context.collect}} is not null flow_id=pattern_collect_information rendered_condition=slots.deposit_amount_gbp is not null
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.link.else_condition_satisfied current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information target=ask_collect
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information next_id=ask_collect
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_2_collect_deposit_amount_gbp', 'collect': 'deposit_amount_gbp', 'utter': 'utter_ask_deposit_amount_gbp', 'collect_action': 'action_ask_deposit_amount_gbp', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=ask_collect
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:44 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - Predicted next action 'utter_ask_deposit_amount_gbp' with confidence 1.00.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_ask_deposit_amount_gbp policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_1_validate_{{context.collect}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "ask_collect"}]""")]
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_ask_deposit_amount_gbp rasa_events=[BotUttered('What deposit amount in GBP are you proposing to secure the booking?', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"active_flow": "confirm_booking", "step_id": "confirm_booking_2_collect_deposit_amount_gbp", "utter_action": "utter_ask_deposit_amount_gbp", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733404.962687)]
2026-04-09 12:16:44 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=ask_collect
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=ask_collect flow_id=pattern_collect_information next_id=pattern_collect_information_3_{{context.collect_action}}
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_3_{{context.collect_action}}
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_3_{{context.collect_action}} flow_id=pattern_collect_information next_id=pattern_collect_information_4_action_listen
2026-04-09 12:16:44 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_2_collect_deposit_amount_gbp', 'collect': 'deposit_amount_gbp', 'utter': 'utter_ask_deposit_amount_gbp', 'collect_action': 'action_ask_deposit_amount_gbp', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=pattern_collect_information_4_action_listen
Let's continue with confirm booking.
2026-04-09 12:16:44 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:16:44 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - Predicted next action 'action_listen' with confidence 1.00.
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_listen policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_3_{{context.collect_action}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_4_action_listen"}]""")]
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_listen rasa_events=[]
2026-04-09 12:16:44 DEBUG    rasa.core.tracker_stores.tracker_store  - [debug    ] No event broker configured. Skipping streaming events. event_key=tracker_store.stream_events.no_broker_configured
2026-04-09 12:16:44 DEBUG    rasa.core.processor  - [debug    ] processor.trigger_anonymization.skipping.pii_management_not_enabled
2026-04-09 12:16:44 DEBUG    rasa.core.lock_store  - [debug    ] Deleted lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._deleted_lock_for_conversation
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  can you arrange parking for the customers                                                                                                                    
2026-04-09 12:17:41 DEBUG    rasa.core.lock_store  - [debug    ] Issuing ticket for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store.issue_ticket
2026-04-09 12:17:41 DEBUG    rasa.core.lock_store  - [debug    ] Acquiring lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._acquiring_lock_for_conversation
2026-04-09 12:17:41 DEBUG    rasa.core.lock_store  - [debug    ] Acquired lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._acquired_lock_for_conversation
2026-04-09 12:17:41 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {}, targets: ['flows_provider'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:17:41 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:17:41 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__message__': [UserMessage(text: can you arrange parking for the customers, sender_id: a8e9d54b848e4ab4ab08d70f1779476e)], '__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e)}, targets: ['run_RegexMessageHandler'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:17:41 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=NLUMessageConverter fn=convert_user_message node_name=nlu_message_converter
2026-04-09 12:17:41 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:17:41 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:17:41 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=CompactLLMCommandGenerator fn=process node_name=run_CompactLLMCommandGenerator0
2026-04-09 12:17:41 DEBUG    rasa.dialogue_understanding.utils  - [debug    ] Tracker doesn't have the 'route_session_to_calm' slot.Routing to CALM. event_key=utils.handle_via_nlu_in_coexistence.tracker_missing_route_session_to_calm_slot route_session_to_calm=[]
2026-04-09 12:17:41 DEBUG    rasa.shared.providers.embedding._base_litellm_embedding_client  - [debug    ] base_litellm_client.formatted_response formatted_response={'data': 'Embedding response data not shown here for brevity.', 'model': 'Qwen/Qwen3-Embedding-8B', 'usage': {'prompt_tokens': 8, 'completion_tokens': 0, 'total_tokens': 8}, 'additional_info': None}
2026-04-09 12:17:41 DEBUG    rasa.dialogue_understanding.generator.flow_retrieval  - [debug    ] Fetched the top 20similar flows from the vector store event_key=flow_retrieval.query_vector_store.fetched query=can you arrange parking for the customers results=[{'flow_id': 'handle_out_of_scope', 'score': 0.7122341, 'content': 'handle out of scope: Handle requests that are outside the scope of booking confirmation, such as questions about parking, AV equipment, seating arrangements, menus, weather, or any non-booking topic.'}, {'flow_id': 'confirm_booking', 'score': 0.703777, 'content': "confirm booking: Handle an inbound call from a pub manager confirming a venue booking for tonight's event. Triggered when the pub manager calls to confirm booking details, including guest count, dietary requirements, and deposit terms. This is the primary task — all booking-related calls should use this flow.\n\n    guest_count: total number of guests attending tonight's event\n    vegan_count: number of guests requiring vegan meals\n    deposit_amount_gbp: deposit amount in GBP the manager is proposing to secure the booking"}] top_k=20
2026-04-09 12:17:41 DEBUG    rasa.dialogue_understanding.generator.llm_based_command_generator  - [debug    ] llm_based_command_generator.predict_commands.filtered_flows enabled_flow_retrieval=True message={'text': 'can you arrange parking for the customers', 'message_id': '8d8378ea6596427bb06a4b99465c8097', 'metadata': None, 'flows_from_semantic_search': [('handle_out_of_scope', 0.7122340798377991), ('confirm_booking', 0.703777015209198)], 'flows_in_prompt': ['confirm_booking', 'handle_out_of_scope']} relevant_flows=['confirm_booking', 'handle_out_of_scope']
2026-04-09 12:17:41 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.prompt_rendered prompt=## Task Description
Your task is to analyze the current conversation context and generate a list of actions to start new business processes that we call flows, to extract slots, or respond to small talk and knowledge requests.

---

## Available Flows and Slots
Use the following structured data:
```json
{"flows":[{"name":"handle_out_of_scope","description":"Handle requests that are outside the scope of booking confirmation, such as questions about parking, AV equipment, seating arrangements, menus, weather, or any non-booking topic.\n"},{"name":"confirm_booking","description":"Handle an inbound call from a pub manager confirming a venue booking for tonight's event. Triggered when the pub manager calls to confirm booking details, including guest count, dietary requirements, and deposit terms. This is the primary task — all booking-related calls should use this flow.\n","slots":[{"name":"guest_count","description":"total number of guests attending tonight's event"},{"name":"vegan_count","description":"number of guests requiring vegan meals"},{"name":"deposit_amount_gbp","description":"deposit amount in GBP the manager is proposing to secure the booking"}]}]}
```

---

## Available Actions:
* `start flow flow_name`: Starting a flow. For example, `start flow transfer_money` or `start flow list_contacts`.
* `set slot slot_name slot_value`: Slot setting. For example, `set slot transfer_money_recipient Freddy`. Can be used to correct and change previously set values.
* `cancel flow`: Cancelling the current flow.
* `disambiguate flows flow_name1 flow_name2 ... flow_name_n`: Disambiguate which flow should be started when user input is ambiguous by listing the potential flows as options. For example, `disambiguate flows list_contacts add_contact remove_contact ...` if the user just wrote "contacts".
* `provide info`: Responding to the user's questions by supplying relevant information, such as answering FAQs or explaining services.
* `offtopic reply`: Responding to casual or social user messages that are unrelated to any flows, engaging in friendly conversation and addressing off-topic remarks.
* `hand over`: Handing over to a human, in case the user seems frustrated or explicitly asks to speak to one.
* `repeat message`: Repeating the last bot message.

---

## General Tips
* Do not fill slots with abstract values or placeholders.
* For categorical slots try to match the user message with allowed slot values. Use "other" if you cannot match it.
* Set the boolean slots based on the user response. Map positive responses to `True`, and negative to `False`.
* Extract text slot values exactly as provided by the user. Avoid assumptions, format changes, or partial extractions.
* Only use information provided by the user.
* Use clarification in ambiguous cases.
* Multiple flows can be started. If a user wants to digress into a second flow, you do not need to cancel the current flow.
* Do not cancel the flow unless the user explicitly requests it.
* Strictly adhere to the provided action format.
* Focus on the last message and take it one step at a time.
* Use the previous conversation steps only to aid understanding.

---

## Current State
Use the following structured data:
```json
{"active_flow":"confirm_booking","current_step":{"requested_slot":"deposit_amount_gbp","requested_slot_description":"deposit amount in GBP the manager is proposing to secure the booking"},"slots":[{"name":"guest_count","value":"160.0","type":"float","description":"total number of guests attending tonight's event"},{"name":"vegan_count","value":"50.0","type":"float","description":"number of guests requiring vegan meals"},{"name":"deposit_amount_gbp","value":"undefined","type":"float","description":"deposit amount in GBP the manager is proposing to secure the booking"}]}
```

---

## Conversation History
USER: calling to confirm a booking
AI: I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
AI: How many guests are you confirming for tonight's event?
USER: 160 guests
AI: And how many of those guests will need vegan meals?
USER: 50 vegan
AI: I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
AI: What deposit amount in GBP are you proposing to secure the booking?
USER: can you arrange parking for the customers?
AI: I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
AI: I'm sorry, I'm not trained to help with that.
AI: I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly. 
AI: Let's continue with confirm booking.
AI: What deposit amount in GBP are you proposing to secure the booking?
USER: can you arrange parking for the customers

---

## Task
Create an action list with one action per line in response to the user's last message: can you arrange parking for the customers
Your action list:Users/PycharmProjects/sovereign-agent-lab/exercise3_rasa/.venv/lib/python3.10/site-packages/pydantic/main.py:441: UserWarning: Pydantic serializer warnings:
  PydanticSerializationUnexpectedValue: Expected 10 fields but got 5 for type `Message` with value `Message(content='start flow handle_out_of_scope\no...None, provider_specific_fields={'refusal': None})` - serialized value may not be as expected.
  PydanticSerializationUnexpectedValue: Expected `StreamingChoices` but got `Choices` with value `Choices(finish_reason='st...one, 'token_ids': None})` - serialized value may not be as expected
  return self.__pydantic_serializer__.to_json(
2026-04-09 12:17:42 DEBUG    rasa.shared.providers.llm._base_litellm_client  - [debug    ] base_litellm_client.formatted_response formatted_response={'id': 'chatcmpl-45317e5da185486485a83290bacebd1e', 'choices': ['start flow handle_out_of_scope\nofftopic reply \nprovide info'], 'created': 1775733461, 'model': 'hosted_vllm/meta-llama/Llama-3.3-70B-Instruct', 'usage': {'prompt_tokens': 1087, 'completion_tokens': 14, 'total_tokens': 1101}, 'additional_info': None, 'latency': None}
2026-04-09 12:17:42 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.actions_generated action_list=start flow handle_out_of_scope
offtopic reply
provide info
2026-04-09 12:17:42 DEBUG    rasa.utils.log_utils  - [debug    ] llm_command_generator.predict_commands.finished commands=[StartFlowCommand(flow='handle_out_of_scope'), ChitChatAnswerCommand(), KnowledgeAnswerCommand()]
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RegexMessageHandler fn=process node_name=run_RegexMessageHandler
2026-04-09 12:17:42 DEBUG    rasa.core.processor  - [debug    ] processor.message.parse        parse_data_entities=[] parse_data_intent={'name': None, 'confidence': 0.0} parse_data_text=can you arrange parking for the customers
2026-04-09 12:17:42 DEBUG    rasa.core.processor  - Logged UserUtterance - tracker now has 123 events.
2026-04-09 12:17:42 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {}, targets: ['flows_provider'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:17:42 DEBUG    rasa.core.processor  - [debug    ] processor.extract.slots        action_extract_slot=action_extract_slots len_extraction_events=0 rasa_events=[]
2026-04-09 12:17:42 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e)}, targets: ['command_processor'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=CommandProcessorComponent fn=execute_commands node_name=command_processor
2026-04-09 12:17:42 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] command_processor.clean_up_commands.prepend_command_chitchat_answer command=ChitChatAnswerCommand() defined_intentless_policy_in_config=False pattern_chitchat_uses_action_trigger_chitchat=False
2026-04-09 12:17:42 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] command_processor.clean_up_commands.prepend_command_freeform_answer command=KnowledgeAnswerCommand()
2026-04-09 12:17:42 DEBUG    rasa.dialogue_understanding.processor.command_processor  - [debug    ] command_processor.clean_up_commands.final_commands command=[KnowledgeAnswerCommand(), ChitChatAnswerCommand(), StartFlowCommand(flow='handle_out_of_scope')]
2026-04-09 12:17:42 DEBUG    rasa.dialogue_understanding.commands.start_flow_command  - [debug    ] start_flow_command.start_flow  command=StartFlowCommand(flow='handle_out_of_scope')
2026-04-09 12:17:42 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:17:42 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_search previous_step_id=START
2026-04-09 12:17:42 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=pattern_search next_id=pattern_search_0_utter_no_knowledge_base
2026-04-09 12:17:42 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'OONX4G9J', 'flow_id': 'pattern_search', 'step_id': 'pattern_search_0_utter_no_knowledge_base', 'type': 'pattern_search'}} flow_id=pattern_search step_id=pattern_search_0_utter_no_knowledge_base
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:17:42 DEBUG    rasa.core.policies.ensemble  - Made prediction using user intent.
2026-04-09 12:17:42 DEBUG    rasa.core.policies.ensemble  - Added `DefinePrevUserUtteredFeaturization(False)` event.
2026-04-09 12:17:42 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:17:42 DEBUG    rasa.core.processor  - Predicted next action 'utter_no_knowledge_base' with confidence 1.00.
2026-04-09 12:17:42 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_no_knowledge_base policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/4/step_id", "value": "pattern_search_0_utter_no_knowledge_base"}]"""), FlowStarted(flow: pattern_search), <rasa.shared.core.events.DefinePrevUserUtteredFeaturization object at 0x29764a350>]
2026-04-09 12:17:42 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_no_knowledge_base rasa_events=[BotUttered('I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"metadata": {"rephrase": true}, "active_flow": "pattern_search", "step_id": "pattern_search_0_utter_no_knowledge_base", "utter_action": "utter_no_knowledge_base", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733462.987713)]
2026-04-09 12:17:42 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:17:42 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_search previous_step_id=pattern_search_0_utter_no_knowledge_base
2026-04-09 12:17:42 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_search_0_utter_no_knowledge_base flow_id=pattern_search next_id=END
2026-04-09 12:17:42 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=pattern_search step_id=END
2026-04-09 12:17:42 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_chitchat previous_step_id=START
2026-04-09 12:17:42 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=pattern_chitchat next_id=pattern_chitchat_0_utter_cannot_handle
2026-04-09 12:17:42 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': '00KTWIPI', 'flow_id': 'pattern_chitchat', 'step_id': 'pattern_chitchat_0_utter_cannot_handle', 'type': 'pattern_chitchat'}} flow_id=pattern_chitchat step_id=pattern_chitchat_0_utter_cannot_handle
2026-04-09 12:17:42 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:17:42 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:17:42 DEBUG    rasa.core.processor  - Predicted next action 'utter_cannot_handle' with confidence 1.00.
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_cannot_handle policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/4/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/4"}]"""), FlowCompleted(flow: pattern_search, step_id: pattern_search_0_utter_no_knowledge_base), DialogueStackUpdate("""[{"op": "replace", "path": "/3/step_id", "value": "pattern_chitchat_0_utter_cannot_handle"}]"""), FlowStarted(flow: pattern_chitchat)]
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_cannot_handle rasa_events=[BotUttered('I'm sorry, I'm not trained to help with that.', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"active_flow": "pattern_chitchat", "step_id": "pattern_chitchat_0_utter_cannot_handle", "utter_action": "utter_cannot_handle", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733463.00084)]
2026-04-09 12:17:43 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_chitchat previous_step_id=pattern_chitchat_0_utter_cannot_handle
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_chitchat_0_utter_cannot_handle flow_id=pattern_chitchat next_id=END
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=pattern_chitchat step_id=END
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=handle_out_of_scope previous_step_id=START
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=handle_out_of_scope next_id=handle_out_of_scope_0_utter_out_of_scope
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'HPKX6V3T', 'flow_id': 'handle_out_of_scope', 'step_id': 'handle_out_of_scope_0_utter_out_of_scope', 'frame_type': 'interrupt', 'type': 'flow'}} flow_id=handle_out_of_scope step_id=handle_out_of_scope_0_utter_out_of_scope
I am afraid, I don't know the answer. At this point, I don't have access to a knowledge base.
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:17:43 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - Predicted next action 'utter_out_of_scope' with confidence 1.00.
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_out_of_scope policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/3/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/3"}]"""), FlowCompleted(flow: pattern_chitchat, step_id: pattern_chitchat_0_utter_cannot_handle), DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "handle_out_of_scope_0_utter_out_of_scope"}]"""), FlowStarted(flow: handle_out_of_scope)]
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_out_of_scope rasa_events=[BotUttered('I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"active_flow": "handle_out_of_scope", "step_id": "handle_out_of_scope_0_utter_out_of_scope", "utter_action": "utter_out_of_scope", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733463.012146)]
2026-04-09 12:17:43 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=handle_out_of_scope previous_step_id=handle_out_of_scope_0_utter_out_of_scope
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=handle_out_of_scope_0_utter_out_of_scope flow_id=handle_out_of_scope next_id=END
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=handle_out_of_scope step_id=END
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_continue_interrupted previous_step_id=START
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=START flow_id=pattern_continue_interrupted next_id=pattern_continue_interrupted_0_utter_flow_continue_interrupted
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'G4AL8UAM', 'flow_id': 'pattern_continue_interrupted', 'step_id': 'pattern_continue_interrupted_0_utter_flow_continue_interrupted', 'previous_flow_name': 'confirm booking', 'type': 'pattern_continue_interrupted'}} flow_id=pattern_continue_interrupted step_id=pattern_continue_interrupted_0_utter_flow_continue_interrupted
I'm sorry, I'm not trained to help with that.
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:17:43 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - Predicted next action 'utter_flow_continue_interrupted' with confidence 1.00.
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_flow_continue_interrupted policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/2/frame_type"}, {"op": "add", "path": "/2/previous_flow_name", "value": "confirm booking"}, {"op": "replace", "path": "/2/step_id", "value": "START"}, {"op": "replace", "path": "/2/type", "value": "pattern_continue_interrupted"}, {"op": "replace", "path": "/2/frame_id", "value": "G4AL8UAM"}, {"op": "replace", "path": "/2/flow_id", "value": "pattern_continue_interrupted"}]"""), FlowCompleted(flow: handle_out_of_scope, step_id: handle_out_of_scope_0_utter_out_of_scope), FlowResumed(flow: confirm_booking, step_id: confirm_booking_2_collect_deposit_amount_gbp), DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "pattern_continue_interrupted_0_utter_flow_continue_interrupted"}]"""), FlowStarted(flow: pattern_continue_interrupted)]
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_flow_continue_interrupted rasa_events=[BotUttered('Let's continue with confirm booking.', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"metadata": {"rephrase": true, "template": "jinja"}, "active_flow": "pattern_continue_interrupted", "step_id": "pattern_continue_interrupted_0_utter_flow_continue_interrupted", "utter_action": "utter_flow_continue_interrupted", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733463.022696)]
2026-04-09 12:17:43 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_continue_interrupted previous_step_id=pattern_continue_interrupted_0_utter_flow_continue_interrupted
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_continue_interrupted_0_utter_flow_continue_interrupted flow_id=pattern_continue_interrupted next_id=END
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.flow_end         flow_id=pattern_continue_interrupted step_id=END
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_4_action_listen
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_4_action_listen flow_id=pattern_collect_information next_id=start
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_2_collect_deposit_amount_gbp', 'collect': 'deposit_amount_gbp', 'utter': 'utter_ask_deposit_amount_gbp', 'collect_action': 'action_ask_deposit_amount_gbp', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=start
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:17:43 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - Predicted next action 'action_run_slot_rejections' with confidence 1.00.
2026-04-09 12:17:43 DEBUG    rasa.core.actions.action_run_slot_rejections  - [debug    ] first.collect.slot.not.set     slot_name=deposit_amount_gbp slot_value=None
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_run_slot_rejections policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/2/step_id", "value": "END"}]"""), DialogueStackUpdate("""[{"op": "remove", "path": "/2"}]"""), FlowCompleted(flow: pattern_continue_interrupted, step_id: pattern_continue_interrupted_0_utter_flow_continue_interrupted), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "start"}]""")]
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_run_slot_rejections rasa_events=[]
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.slots.log            slots={'language': 'en', 'silence_timeout': 7.0, 'consecutive_silence_timeouts': 0.0, 'guest_count': 160.0, 'vegan_count': 50.0, 'flow_hashes': {'confirm_booking': '0cfdd2e66537a1c1dc08453deb2ae383', 'handle_out_of_scope': '367e697b00b1da958c811004266f6c46', 'pattern_cancel_flow': '5edee5445ff87339ec899ab96de7ae9e', 'pattern_cannot_handle': '748dcc3783183f4c5512c2f23940b609', 'pattern_chitchat': 'aabaace3f5ef32b70351e18481c53356', 'pattern_clarification': '927f334af1fe5e570348690977bac4f2', 'pattern_code_change': 'f9db9f453c8b63fbec24c72413c86a69', 'pattern_collect_information': '072cd971740a761ddb8885f2cdc6ff20', 'pattern_completed': 'df3529f96e5d98df3f2ce63012daa641', 'pattern_continue_interrupted': '61bf7886bc116521c0d8f6f5b6760e67', 'pattern_correction': 'c35924757a8df574b91355c9a2070931', 'pattern_human_handoff': 'c021df067d37b8a23c464ca92372df6c', 'pattern_internal_error': 'b9059f3a7ca73e38b1d19ad0b09c9537', 'pattern_repeat_bot_messages': '35069cf740ceaff65ac467a58c3f77bf', 'pattern_restart': '9f4c81ddc0dcb8c4a74a141a047f0284', 'pattern_search': 'cf65ab2f7654f41f481a5f97cbcb9d9d', 'pattern_session_start': '757ea1cd44b685619e46d9c7b32c30b8', 'pattern_skip_question': '46505c0a24a5f90ab6f58a1fc69fa41b', 'pattern_user_silence': '41f05270eba1765c2fd9f1b17e1d754a', 'pattern_validate_slot': '57e5983e77f386ff93dfdcbad1c93308'}}
2026-04-09 12:17:43 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=start
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=start flow_id=pattern_collect_information next_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_1_validate_{{context.collect}}
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.predicate.evaluating      condition=slots.{{context.collect}} is not null flow_id=pattern_collect_information rendered_condition=slots.deposit_amount_gbp is not null
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.link.else_condition_satisfied current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information target=ask_collect
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_1_validate_{{context.collect}} flow_id=pattern_collect_information next_id=ask_collect
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_2_collect_deposit_amount_gbp', 'collect': 'deposit_amount_gbp', 'utter': 'utter_ask_deposit_amount_gbp', 'collect_action': 'action_ask_deposit_amount_gbp', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=ask_collect
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:17:43 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - Predicted next action 'utter_ask_deposit_amount_gbp' with confidence 1.00.
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=utter_ask_deposit_amount_gbp policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_1_validate_{{context.collect}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "ask_collect"}]""")]
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=utter_ask_deposit_amount_gbp rasa_events=[BotUttered('What deposit amount in GBP are you proposing to secure the booking?', {"elements": null, "quick_replies": null, "buttons": null, "attachment": null, "image": null, "custom": null}, {"active_flow": "confirm_booking", "step_id": "confirm_booking_2_collect_deposit_amount_gbp", "utter_action": "utter_ask_deposit_amount_gbp", "utter_source": "TemplatedNaturalLanguageGenerator"}, 1775733463.041573)]
2026-04-09 12:17:43 DEBUG    rasa.engine.runner.dask  - Running graph with inputs: {'__tracker__': DialogueStateTracker(sender_id: a8e9d54b848e4ab4ab08d70f1779476e), '__endpoints__': <rasa.core.available_endpoints.AvailableEndpoints object at 0x16e237520>}, targets: ['select_prediction'] and ExecutionContext(model_id='35a78780631e404ca6d12a29a0aecf5b', should_add_diagnostic_data=False, is_finetuning=False, node_name=None).
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=RuleOnlyDataProvider fn=provide node_name=rule_only_data_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DomainProvider fn=provide_inference node_name=domain_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowsProvider fn=provide_inference node_name=flows_provider
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=FlowPolicy fn=predict_action_probabilities node_name=run_FlowPolicy0
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=ask_collect
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=ask_collect flow_id=pattern_collect_information next_id=pattern_collect_information_3_{{context.collect_action}}
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.execution.loop            flow_id=pattern_collect_information previous_step_id=pattern_collect_information_3_{{context.collect_action}}
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.next                 current_id=pattern_collect_information_3_{{context.collect_action}} flow_id=pattern_collect_information next_id=pattern_collect_information_4_action_listen
2026-04-09 12:17:43 DEBUG    rasa.core.policies.flows.flow_executor  - [debug    ] flow.step.run.action           context={'context': {'frame_id': 'ORHSA6KM', 'flow_id': 'confirm_booking', 'step_id': 'confirm_booking_2_collect_deposit_amount_gbp', 'collect': 'deposit_amount_gbp', 'utter': 'utter_ask_deposit_amount_gbp', 'collect_action': 'action_ask_deposit_amount_gbp', 'rejections': [], 'type': 'flow', 'frame_type': 'regular'}} flow_id=pattern_collect_information step_id=pattern_collect_information_4_action_listen
Let's continue with confirm booking.
2026-04-09 12:17:43 DEBUG    rasa.engine.graph  - [debug    ] graph.node.running_component   clazz=DefaultPolicyPredictionEnsemble fn=combine_predictions_from_kwargs node_name=select_prediction
2026-04-09 12:17:43 DEBUG    rasa.core.policies.ensemble  - Predicted next action using FlowPolicy.
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - Predicted next action 'action_listen' with confidence 1.00.
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.actions.policy_prediction action_name=action_listen policy_name=FlowPolicy prediction_events=[DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_3_{{context.collect_action}}"}]"""), DialogueStackUpdate("""[{"op": "replace", "path": "/1/step_id", "value": "pattern_collect_information_4_action_listen"}]""")]
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.actions.log          action_name=action_listen rasa_events=[]
2026-04-09 12:17:43 DEBUG    rasa.core.tracker_stores.tracker_store  - [debug    ] No event broker configured. Skipping streaming events. event_key=tracker_store.stream_events.no_broker_configured
2026-04-09 12:17:43 DEBUG    rasa.core.processor  - [debug    ] processor.trigger_anonymization.skipping.pii_management_not_enabled
2026-04-09 12:17:43 DEBUG    rasa.core.lock_store  - [debug    ] Deleted lock for conversation 'a8e9d54b848e4ab4ab08d70f1779476e'. event_key=lock_store._deleted_lock_for_conversation
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  /Users//miniconda3/envs/VM_Review_Agent/lib/python3.10/asyncio/sslproto.py:320: ResourceWarning: unclosed transport <asyncio.sslproto._SSLProtocolTransport object at 0x2971bfdc0>
  _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/Users//miniconda3/envs/VM_Review_Agent/lib/python3.10/asyncio/sslproto.py:320: ResourceWarning: unclosed transport <asyncio.sslproto._SSLProtocolTransport object at 0x2972a0e20>
  _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
Your input -> """

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """ CALM recognised the question is out ofscope and decided to continue the flow by repeating the\
question of how mcuh deposit I can retain. In the old behaciour if the question was out of scope the conversation would have ben terminated,

"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
LangGraph handled the out-of-scope train question by generating a natural, 
human-like response — it acknowledged the question, explained it couldn't 
help with train schedules, and suggested where to find the information. 
The response felt conversational and contextually aware.

Rasa CALM, by contrast, silently continued the confirm_booking flow and 
asked for the deposit amount without acknowledging the parking question at 
all. It prioritised task completion over conversational naturalness.

This reflects a fundamental architectural difference: LangGraph gives the 
LLM full freedom to respond to anything at any point, making it more 
flexible and human-like. Rasa CALM constrains the LLM to defined flows, 
making it more predictable and auditable but less conversational
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE =True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["""changed the threshold £ on the actions file.\
I also have to change the time 4.45 as if I run the script after that time it triggers the exception"""]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
through debugging.tested the overall behaviour before and after teh change remained the same apart from the\
change in the above scripts.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
With CALM the code becomes simpler as we not longer have to give explicit phrases and sample to thyml file. as with olf RASA\
in CALM the LLM handles query extracts the numbers and initiates the flow.There are not strict rules and policies to maintain.\
this  also  means the  response can be less predictable and with less control which means less auditable and less consistency at the testing level

Think about:
- What does the LLM handle now that Python handled before?
- What does Python STILL handle, and why (hint: business rules)?
- Is there anything you trusted more in the old approach?
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
CALM cannot improvise and call other tools outside from its defined workflow, so cannot call the weather app , train \
schedule etc. Also even for the defined workflow it cannot reverse order. It is actually very deterministic and unflexible.
It may come with  some benefit around consistency so for instance cannot improvise around a deposit transaction\
but at the same time if I were a customer this workflow is very single directed and unflexible as it cannot handle exceptions, edge cases etc.
 Langraphs uses the whole knowledge base of the LLM so responses are far more realistic and helful but it may come\with some risk arounr\
 hallucination or problems on customer service and audit especialy when dealing with fiannce.

Be specific. What can the Rasa CALM agent NOT do that LangGraph could?
Is that a feature or a limitation for the confirmation use case?
Think about: can the CALM agent improvise a response it wasn't trained on?
Can it call a tool that wasn't defined in flows.yml?
"""
