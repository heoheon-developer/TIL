package member;

public class Member {
	//Todo 일반 회원 클래스의 속성은 아이디, 이름, 등급(FAMILY) 세가지 입니다.
	int memberId;
	String memberName;
	String rank;
	
	
	public Member() {
	//To-do 일반 멤버의 기본 등급을 FAMILY로 만들어 줍니다.
		this.rank = "FAMILY";
	}
	
	public Member(int memberId, String memberName) {
		this.memberId = memberId;
		this.memberName = memberName;
	}
	
	
	// To-do 일반 회원 클래스의 각 속성에 getter/setter를 제공합니다.
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
		sb.append("[일반회원] = ");
		sb.append("1.회원아이디 : " + this.getMemberId() +", ");
		sb.append("2.회원이름 : " + this.getMemberName());
		
		return sb.toString();

	}

	
	
	//To-do 회원을 이름 순으로 정렬하기 위해 Comparable 메서드를 구현합니다.
	
	

	
}
