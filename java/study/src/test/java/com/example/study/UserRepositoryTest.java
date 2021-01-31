package com.example.study;

import com.example.study.model.entity.User;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import com.example.study.repository.UserRepository;

import java.time.LocalDateTime;

public class UserRepositoryTest extends StudyApplicationTests{


    @Autowired
    private UserRepository userRepository;

    @Test
    public void create(){

        User user = new User();

        user.setAccount("TestUser01");
        user.setEmail("TestUser01@gmail.com");
        user.setPhoneNumber("010-5321-2456");
        user.setCreateAt(LocalDateTime.now());
        user.setCreateBy("admin");

        User newUser = userRepository.save(user);

        System.out.print("newUser :" +newUser );

    }

    public void read(){


    }

    public void update(){

    }

    public void delete(){

    }
}
