package member;

public class VIPMember extends Member{
	// To-do VIPMember�� Member���� ����� �޽��ϴ�.
	// To-do ���� ���� ���̵� �Ӽ��� �߰��մϴ�
	
	int memberId;
	String memberName;
	int agentId;
	String rank;
	
	public VIPMember() {
		// To-do ����� VIP�� ������ �ݴϴ�.		
		this.rank = "VIP";
		
	}
	
	public VIPMember(int memberId, String memberName, int agentId) {
		this.memberId = memberId;
		this.memberName = memberName;
		this.agentId = agentId;		
		// To-do
	}
	
	public String showMemberInfo() {
		// To-do VIP ������ �����ִ� showMemberInfo �޼��带 �������ϰ�, ���� ������ �����ֵ��� �մϴ�		
		
		StringBuilder sb = new StringBuilder();
		sb.append("[VIPȸ��] = ");
		sb.append("1.ȸ�����̵� : " + this.getMemberId() +", ");
		sb.append("2.ȸ���̸� : " + this.getMemberName() +", ");
		sb.append("3.���� ���� : " + this.getAgentId() +"");
		
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



