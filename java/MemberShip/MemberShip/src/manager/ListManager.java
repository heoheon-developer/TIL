package manager;

import java.util.ArrayList;
import java.util.List;

import member.Member;

public class ListManager {

	private ArrayList<Member> memberList;
	//To-do ȸ�� ������ ���� ArrayList�� Ȱ���ϰ�, ȸ���� �߰�,����, ���ȸ���� �����ִ� ������ ����� �����մϴ�.

	
	
	//To-do �����ڸ� ���� ���ο� �������Ʈ�� ����ϴ�.
	public ListManager() {		
		this.memberList = new ArrayList<Member>();		
	}
	
	//To-do ȸ���� �߰��ϴ� �޼��带 ����ϴ�.
	public void addMember(Member member) {		
		memberList.add(member);		
	}
	
	//To-do ȸ���� �����ϴ� �޼��带 ����ϴ�.
	public void removeMember(Member member) {		
		memberList.remove(member);		
	}
	
	//To-do ��� ȸ���� �����ִ� �޼��带 ���� �մϴ�.
	public void printMember(Member member) {		
		System.out.println(member.showMemberInfo());
	}

	public void showAllMember() {
		for(Member member : this.memberList) {				
			this.printMember(member);			
		}		
	}

	public List<Member> getMemberList() {
		return this.memberList;
	}
	//To-do ȸ�������� �������� getter�� �����մϴ�.
}
