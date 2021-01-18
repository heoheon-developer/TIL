package member;

public class VIPMember extends Member{
	// To-do VIPMember는 Member에서 상속을 받습니다.
	// To-do 전담 상담원 아이디 속성을 추가합니다
	
	int memberId;
	String memberName;
	int agentId;
	String rank;
	
	public VIPMember() {
		// To-do 등급을 VIP로 설정해 줍니다.		
		this.rank = "VIP";
		
	}
	
	public VIPMember(int memberId, String memberName, int agentId) {
		this.memberId = memberId;
		this.memberName = memberName;
		this.agentId = agentId;		
		// To-do
	}
	
	public String showMemberInfo() {
		// To-do VIP 정보를 보여주는 showMemberInfo 메서드를 재정의하고, 상담원 정보도 보여주도록 합니다		
		
		StringBuilder sb = new StringBuilder();
		sb.append("[VIP회원] = ");
		sb.append("1.회원아이디 : " + this.getMemberId() +", ");
		sb.append("2.회원이름 : " + this.getMemberName() +", ");
		sb.append("3.전담 상담원 : " + this.getAgentId() +"");
		
		return sb.toString();
		
	}

	public int getMemberId() {
		return memberId;
	}

	public void setMemberId(int memberId) {
		this.memberId = memberId;
	}

	public String getMemberName() {
		return memberName;
	}

	public void setMemberName(String memberName) {
		this.memberName = memberName;
	}

	public int getAgentId() {
		return agentId;
	}

	public void setAgentId(int agentId) {
		this.agentId = agentId;
	}

	public String getRank() {
		return rank;
	}

	public void setRank(String rank) {
		this.rank = rank;
	}

	
	
	
	
}



