package repository;

import hello.hellospring.domain.Member;
import hello.hellospring.repository.MemberRepository;
import hello.hellospring.repository.MemoryMemberRepository;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;

public class MemoryMemberRepositoryTest {


    MemberRepository repository = new MemoryMemberRepository();



    @Test
    public void save(){

        Member member = new Member();
        member.setName("Test");

        repository.save(member);

        Member result = repository.findById(member.getId()).get();


        System.out.println(result);

        Assertions.assertThat(member).isEqualTo(null);

    }




}
