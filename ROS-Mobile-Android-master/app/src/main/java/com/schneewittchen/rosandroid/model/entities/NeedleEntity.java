package com.schneewittchen.rosandroid.model.entities;

import androidx.room.Entity;
import androidx.room.PrimaryKey;


/**
 * TODO: Description
 *
 * @author Nico Studt
 * @version 1.0.1
 * @created on 30.01.20
 * @updated on 31.01.20
 * @modified by
 */
@Entity(tableName = "needle_table")
public class NeedleEntity {

    @PrimaryKey(autoGenerate = true)
    public long id;

    public float distance = 0;
}
