from langchain_core.messages import HumanMessage

class ChatInterface:
    
    def __init__(self, rag_system):
        self.rag_system = rag_system
        
    async def chat(self, message, history):

        if not self.rag_system.agent_graph:
            return "System not initialized!"
            
        try:
            current_config = self.rag_system.get_config()
            current_state = self.rag_system.agent_graph.get_state(current_config)
            if current_state.next:
                self.rag_system.agent_graph.update_state(current_config,{"messages": [HumanMessage(content=message.strip())]})
                result = await self.rag_system.agent_graph.ainvoke(None, current_config)
            else:
                result = await self.rag_system.agent_graph.ainvoke(
                    {"messages": [HumanMessage(content=message.strip())]}, current_config
                )
            return result["messages"][-1].content
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_session(self):
        self.rag_system.reset_thread()