package com.example.study;

import com.example.study.model.entity.User;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import com.example.study.repository.UserRepository;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Optional;

public class UserRepositoryTest extends StudyApplicationTests{


    @Autowired
    private UserRepository userRepository;

    @Test
    public void create(){

        User user = new User();

        user.setAccount("TestUser01");
        user.setEmail("TestUser01@gmail.com");
        user.setPhoneNumber("010-5321-2456");
        user.setCreatedAt(LocalDateTime.now());
        user.setCreatedBy("admin");

        User newUser = userRepository.save(user);

        System.out.print("newUser :" +newUser );

    }

    @Test
    public void read(){

        Optional<User> user = userRepository.findById(2L);
        user.ifPresent(selectUser ->{
            System.out.print("user :" + selectUser);
        });
    }

    @Test
    public void update(){
        Optional<User> user = userRepository.findById(2L);
        user.ifPresent(selectUser ->{
           selectUser.setAccount("PPPP");
           selectUser.setUpdatedAt(LocalDateTime.now());
           selectUser.setUpdatedBy("heoheon");
           userRepository.save(selectUser);
        });
    }

    @Test
    @Transactional
    public void delete(){
        Optional<User> user = userRepository.findById(1L);

        user.ifPresent(selectUser ->{

            userRepository.delete(selectUser);
        });

        Optional<User> deleteUser = userRepository.findById(1L);

        if(deleteUser.isPresent()){

            System.out.println("데이터 존재:" + deleteUser.get());
        }else{
            System.out.println("데이터 삭제 데이터 없음");
        }






    }
}
