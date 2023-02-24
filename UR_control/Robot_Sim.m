dhparams = [0 pi/2 0.15185 0;
            -0.24355 0 0 0;
            -0.2132 0 0 0;
            0 pi/2 0.13105 0;
            0 (-pi)/2 0.08535 0;
            0 0 0.0921 0;
            0 0 0.1 0];

robot = rigidBodyTree;

bodies = cell(7,1);
joints = cell(7,1);
for i = 1:7
    bodies{i} = rigidBody(['body' num2str(i)]);
    joints{i} = rigidBodyJoint(['jnt' num2str(i)],"revolute");
    setFixedTransform(joints{i},dhparams(i,:),"dh");
    bodies{i}.Joint = joints{i};
    if i == 1 % Add first body to base
        addBody(robot,bodies{i},"base")
    else % Add current body to previous body by name
        addBody(robot,bodies{i},bodies{i-1}.Name)
    end
end

figure(Name="UR3 robot")
show(robot);