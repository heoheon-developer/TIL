package member;

public class Member {
	//Todo �Ϲ� ȸ�� Ŭ������ �Ӽ��� ���̵�, �̸�, ���(FAMILY) ������ �Դϴ�.
	int memberId;
	String memberName;
	String FAMILY;
	
	
	public Member() {
	//To-do �Ϲ� ����� �⺻ ����� FAMILY�� ����� �ݴϴ�.
		this.FAMILY = FAMILY;
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
	

	public String showMemberInfo() {
		// To-do ȸ�� ������ �����ִ� showMemberInfo �޼��带 �����մϴ�.
		
		
		
		
		
		return "showMemberInfo";
	}

	
	
	//To-do ȸ���� �̸� ������ �����ϱ� ���� Comparable �޼��带 �����մϴ�.
	
	

	
}
