package member;

public class Member {
	//Todo �Ϲ� ȸ�� Ŭ������ �Ӽ��� ���̵�, �̸�, ���(FAMILY) ������ �Դϴ�.
	int memberId;
	String memberName;
	String rank;
	
	
	public Member() {
	//To-do �Ϲ� ����� �⺻ ����� FAMILY�� ����� �ݴϴ�.
		this.rank = "FAMILY";
	}
	
	public Member(int memberId, String memberName) {
		this.memberId = memberId;
		this.memberName = memberName;
	}
	
	
	// To-do �Ϲ� ȸ�� Ŭ������ �� �Ӽ��� getter/setter�� �����մϴ�.
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
	
	
	

	public String getRank() {
		return rank;
	}

	public void setRank(String rank) {
		this.rank = rank;
	}

	public String showMemberInfo() {
		StringBuilder sb = new StringBuilder();
		sb.append("[�Ϲ�ȸ��] = ");
		sb.append("1.ȸ�����̵� : " + this.getMemberId() +", ");
		sb.append("2.ȸ���̸� : " + this.getMemberName());
		
		return sb.toString();

	}

	
	
	//To-do ȸ���� �̸� ������ �����ϱ� ���� Comparable �޼��带 �����մϴ�.
	
	

	
}
