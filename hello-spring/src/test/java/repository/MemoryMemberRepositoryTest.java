package repository;

import hello.hellospring.domain.Member;
import hello.hellospring.repository.MemberRepository;
import hello.hellospring.repository.MemoryMemberRepository;
import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

public class MemoryMemberRepositoryTest {


    MemberRepository repository = new MemoryMemberRepository();


    @Test
    public void save() {

        Member member = new Member();
        member.setName("Test");

        repository.save(member);

        Member result = repository.findById(member.getId()).get();


        System.out.println(result);

        assertThat(member).isEqualTo(result);

    }

    @Test
    public void findByName(){
        Member member1 = new Member();
        member1.setName("spring1");
        repository.save(member1);

        Member member2 = new Member();
        member2.setName("spring2");
        repository.save(member2);


        Member result =  repository.findByName("spring1").get();

        assertThat(result).isEqualTo(member2);


    }


}
