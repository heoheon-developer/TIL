package com.example.study;

import com.example.study.model.entity.OrderDetail;
import com.example.study.repository.OrderDetailRepository;
import org.junit.jupiter.api.Test;


import java.time.LocalDateTime;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;

public class OrderDetailRepositoryTest extends StudyApplicationTests {


    @Autowired
    private OrderDetailRepository orderDetailRepository;

    @Test
    public void create() {

        OrderDetail orderDetail = new OrderDetail();

        orderDetail.setOrderAt(LocalDateTime.now());



        OrderDetail newOrderDetail = orderDetailRepository.save(orderDetail);

        System.out.println("order reposity:" + newOrderDetail);




    }


}
