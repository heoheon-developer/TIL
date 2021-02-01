package com.example.study;

import com.example.study.model.entity.Item;
import com.example.study.repository.ItemRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.Assert;

import static org.junit.jupiter.api.Assertions.*;


public class ItemRepositoryTest extends StudyApplicationTests{

    @Autowired
    private ItemRepository itemRepository;

    @Test
    public void create(){


        Item item = new Item();

        item.setName("Notebook");
        item.setPrice(10000);
        item.setContent("samsung");

        Item newItem = itemRepository.save(item);

        System.out.println("item:" + newItem);




    }
}
